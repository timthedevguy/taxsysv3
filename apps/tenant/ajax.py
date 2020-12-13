import json
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
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
from .models import Character


def ajax_get_director_char_count(request, tenant_id):
    count = Character.objects.filter(user=request.user).count()
    return JsonResponse({'count': count}, safe=False)