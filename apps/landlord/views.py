from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from ..tenant.models import Tenant, Corporation
from ..testesi import testesi_client
from django.conf import settings


# Create your views here.
class IndexView(TemplateView):
    template_name = 'landlord_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tenants = Tenant.objects.all()
        context['tenants'] = tenants
        return context
