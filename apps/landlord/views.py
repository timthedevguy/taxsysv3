from django.shortcuts import render
from django.views.generic import TemplateView
from ..tenant.models import Tenant, Corporation


# Create your views here.
class IndexView(TemplateView):
    template_name = 'landlord_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tenants = Tenant.objects.all()
        context['tenants'] = tenants
        return context


class DirectorSuccess(TemplateView):
    template_name = 'director_success.html'