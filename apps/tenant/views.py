import json
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from apps.testesi.utils import TestClient
from django.conf import settings
from django.http import JsonResponse


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

        if request.user.is_stale:
            return redirect('alt-refresh-error')

        return super().get(request, test='nope', *args, **kwargs)


class SyncErrorView(TemplateView):
    template_name = 'tenant_sync_error.html'


class AltRefreshView(TemplateView):
    template_name = 'tenant_alt_refresh.html'

    def get(self, request, *args, **kwargs):
        # Get Characters
        access_token = TestClient.get_access_token(request)
        data = TestClient.get(settings.TESTESI_GET_CHARACTERS, access_token, subject=request.user.subject)
        return super().get(request, characters=json.dumps(data['characters']), *args, **kwargs)


def ajax_get_alt_info(request):
    test = request.POST.getlist('characters[]')
    return JsonResponse()