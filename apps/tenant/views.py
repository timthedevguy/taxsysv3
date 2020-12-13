import json
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.conf import settings
from django.http import JsonResponse, Http404
from .models import Tenant
from apps.testesi import testesi_client
from .tasks import get_director_details
from huey.contrib import djhuey
import logging
from secrets import token_urlsafe
from .mixins import TenantPermissionRequireMixin
from ..eveonline import esi


# Create your views here.
class IndexView(TemplateView):
    template_name = 'tenant_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            tenant = Tenant.objects.get(identifier=context['tenant_id'])
        except ObjectDoesNotExist:
            raise Http404('Tenant not found')

        # Verify our Token
        if tenant.token != self.request.GET['token']:
            raise PermissionDenied

        # Set User as Admin for their Tenant
        try:
            admin_group = Group.objects.get(name=f'{tenant.name} Administrators')
            admin_group.user_set.add(self.request.user)
        except ObjectDoesNotExist:
            # TODO Handle Exception
            pass

        # Generate new token to invalidate the link
        tenant.token = token_urlsafe()
        tenant.save()

        # Get Characters
        characters = testesi_client.get_characters(subject=self.request.user.subject)
        context['character_count'] = len(characters['characters'])
        context['tenant'] = tenant

        # Queue up the Huey Task to retrieve Character/Corporation Information
        get_director_details(user=self.request.user, characters=characters['characters'], tenant_pk=tenant.id)

        return context


def ajax_get_characters(request):
    characters = testesi_client.get_characters(request.user.subject)
    return JsonResponse(characters, safe=False)


def ajax_get_character_info(request, character_id):
    character = testesi_client.get_character(character_id)
    return JsonResponse(character, safe=False)


def ajax_test(request, tenant_id):
    return JsonResponse({'message': 'Call Finished'}, safe=False)


class TenantAdminIndex(TenantPermissionRequireMixin, TemplateView):
    permission_required = 'admin'
    template_name = 'tenant_admin_index.html'
