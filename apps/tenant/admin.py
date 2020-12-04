from django.contrib import admin
from .models import Tenant, Corporation
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path


# Register your models here.
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'identifier',
        'tenant_actions'
    )
    readonly_fields = (
        'tenant_actions',
        'id'
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:account_id>/corporation/', self.admin_site.admin_view(self.add_corporation), name='add-corporation')
        ]
        return custom_urls + urls



    def tenant_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Add Corporation</a>',
            reverse('admin:add-corporation', args=[obj.pk])
        )

    def add_corporation(self, request, account_id, *args, **kwargs):
        pass

    tenant_actions.short_description = 'Tenant Actions'
    tenant_actions.allow_tags = True
    pass


class CorporationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Corporation, CorporationAdmin)
