import json
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse, Http404
from .models import Tenant
from apps.testesi import testesi_client
from .tasks import test_task
from huey.contrib import djhuey
import logging
from secrets import token_urlsafe

logger = logging.getLogger(__name__)


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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

        # Generate new token to invalidate the link
        tenant.token = token_urlsafe()
        tenant.save()

        return context


def ajax_get_characters(request):
    characters = testesi_client.get_characters(request.user.subject)
    return JsonResponse(characters, safe=False)


# alliance_id: 498125261
# ancestry_id: 14
# birthday: "2018-08-02T22:55:21Z"
# bloodline_id: 7
# corporation_id: 728517421
# description: ""
# gender: "male"
# name: "Pishit X"
# race_id: 8
# security_status: 0
def ajax_get_character_info(request, character_id):
    character = testesi_client.get_character(character_id)
    return JsonResponse(character, safe=False)


def ajax_test(request, tenant_id):
    logger.critical('Task Started in Ajax Test')
    test_task()
    return JsonResponse({'message': 'Call Finished'}, safe=False)
