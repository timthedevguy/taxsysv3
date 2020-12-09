from django.contrib import admin
from .models import Tenant, Corporation
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
import uuid


# Register your models here.
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'token',
        'login_url'
    )

    readonly_fields = (
        'id',
        'token',
        'identifier'
    )

    # Get our Request object to generate the absolute url for admin view
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.request = request
        return qs

    def login_url(self, obj):
        return self.request.build_absolute_uri(reverse('director_login', args=[obj.token]))

    login_url.short_description = 'Director Login URL'

    # def save_model(self, request, obj, form, change):
    #     # Generate a UUID4 as a Unique Identifier for this tenant,
    #     # used in Director Login URL
    #     if obj.identifier == '':
    #         obj.identifier = uuid.uuid4()
    #     super().save_model(request, obj, form, change)


class CorporationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Corporation, CorporationAdmin)
