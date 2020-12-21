import json
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, UpdateView
from .forms import SettingForm
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.http import JsonResponse, Http404
from .models import Tenant
from apps.testesi import testesi_client
from apps.testauth.models import TestUser
from .tasks import get_director_details
from huey.contrib import djhuey
import logging
from secrets import token_urlsafe
from .mixins import TenantPermissionRequireMixin, TenantContextMixin
import re
from .models import Corporation, Tenant, Setting, Character
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_perms = self.request.user.get_all_permissions()
        tenants = []
        missing = []

        # Find tenants that user is Admin of
        for user_perm in user_perms:
            if 'tenant.tenant_' in user_perm:
                m = re.search(
                    '^tenant\.tenant_(?P<tenant_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})_ceo$',
                    user_perm)
                if m is not None:
                    if len(m.groups()) == 1:
                        if m.group(1) not in tenants:
                            tenants.append(m.group(1))

        tenants = Tenant.objects.filter(pk__in=tenants)

        for tenant in tenants:
            if len(tenant.corporations()) == 0:
                missing.append(tenant)

        if len(missing) > 0:
            context['missing'] = missing

        if self.request.user.is_superuser:
            context['tenants'] = Tenant.objects.all()

        return context

    def get(self, request, *args, **kwargs):
        # Check if Auth account is 'Synchronized'
        if not request.user.is_sync:
            return redirect('sync-error')

        # if request.user.is_stale:
        #     return redirect('sync-error')

        return super().get(request, test='nope', *args, **kwargs)


class SyncErrorView(TemplateView):
    template_name = 'tenant_sync_error.html'


def ajax_get_alt_info(request):
    test = request.POST.getlist('characters[]')
    return JsonResponse()


class ProfileView(TemplateView):
    template_name = 'tenant_profile.html'


class DirectorSuccess(TemplateView):
    template_name = 'director_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get tenant
        try:
            tenant = Tenant.objects.get(pk=context['tenant_id'])
        except ObjectDoesNotExist:
            raise Http404('Tenant not found')

        # Verify our Token
        if tenant.token != self.request.GET['token']:
            raise PermissionDenied

        # Setup Permissions
        try:
            # Add user to Administrators Group for the Tenant
            admin_group = Group.objects.get(name=f'{tenant.name} Administrators')
            admin_group.user_set.add(self.request.user)

            # Give them the CEO Permission
            ceo_perm = Permission.objects.get(codename=f'tenant_{tenant.id}_ceo')
            self.request.user.user_permissions.add(ceo_perm)
        except ObjectDoesNotExist:
            # TODO Handle Exception
            pass

        # Generate Default settings for the tenant
        tenant_settings = Setting.objects.create(tenant=tenant)

        # Generate new token to invalidate the link
        tenant.token = token_urlsafe()
        tenant.save()

        # Get Characters
        characters = testesi_client.get_characters(subject=self.request.user.subject)
        context['character_count'] = len(characters['characters'])
        context['tenant'] = tenant

        # Queue up the Huey Task to retrieve Character/Corporation Information
        get_director_details(user=self.request.user, characters=characters['characters'])

        return context


def ajax_get_characters(request):
    characters = testesi_client.get_characters(request.user.subject)
    return JsonResponse(characters, safe=False)


def ajax_get_character_info(request, character_id):
    character = testesi_client.get_character(character_id)
    return JsonResponse(character, safe=False)


def ajax_test(request, tenant_id):
    return JsonResponse({'message': 'Call Finished'}, safe=False)


class TenantIndex(TenantContextMixin, TemplateView):
    template_name = 'tenant_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'wizard' in self.request.GET:
            if self.request.GET['wizard'] == 'False':
                self.request.session.pop('wizard')

        return context


class TenantAdminIndex(TenantPermissionRequireMixin, TenantContextMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'admin'
    template_name = 'tenant_admin_index.html'
    form_class = SettingForm
    success_message = 'Settings updated!'

    def get_object(self, queryset=None):
        return Setting.objects.get(tenant_id=self.kwargs['tenant_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'wizard' in self.request.GET:
            if self.request.GET['wizard'] == 'True':
                self.request.session['wizard'] = True
            else:
                self.request.session.pop('wizard')

        return context


class TenantAdminCorporations(TenantPermissionRequireMixin, TenantContextMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'tenant_admin_corporations.html'


class TenantAdminOverrides(TenantPermissionRequireMixin, TenantContextMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'tenant_admin_overrides.html'


class TenantAdminEvaders(TenantPermissionRequireMixin, TenantContextMixin, TemplateView):
    permission_required = 'auditor'
    template_name = 'tenant_admin_evaders.html'


class TenantAdminLedger(TenantPermissionRequireMixin, TenantContextMixin, TemplateView):
    permission_required = 'accountant'
    template_name = 'tenant_admin_ledger.html'


class TenantAdminUsers(TenantPermissionRequireMixin, TenantContextMixin, TemplateView):
    permission_required = 'accountant'
    template_name = 'tenant_admin_users.html'


class TenantAdminDirectors(TenantPermissionRequireMixin, TenantContextMixin, TemplateView):
    permission_required = 'ceo'
    template_name = 'tenant_admin_director.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        directors = []
        tenant_id = context['tenant_id']
        ceo_perm = Permission.objects.filter(codename=f'tenant_{tenant_id}_ceo')[0]
        ceo_users = TestUser.objects.filter(Q(user_permissions=ceo_perm)).distinct()

        for ceo_user in ceo_users:
            characters = Character.objects.filter(user=ceo_user)
            for character in characters:
                if character.corporation.ceo_id == character.character_id:
                    directors.append({
                        'auth_account': ceo_user.display_name,
                        'corporation': character.corporation.name,
                        'character': character.name
                    })

        context['directors'] = directors

        return context
