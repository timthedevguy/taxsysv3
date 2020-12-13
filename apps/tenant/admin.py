from django.contrib import admin
from .models import Tenant, Corporation
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
import uuid
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


# Register your models here.
class TenantAdmin(admin.ModelAdmin):
    change_list_template = 'tenant_change_list.html'

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

    def save_model(self, request, obj, form, change):
        if not change:
            self.create_perms(obj)

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        self.delete_perms(obj)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_perms(obj)

        super().delete_queryset(request, queryset)

    def create_perms(self, obj):
        # Adding new Tenant, create Permission Objects
        content_type = ContentType.objects.get(app_label='tenant', model='tenant')
        permission_admin = Permission.objects.create(codename=f'tenant_{obj.identifier}_admin',
                                                     name=f'{obj.name} Admin',
                                                     content_type=content_type)
        permission_accountant = Permission.objects.create(codename=f'tenant_{obj.identifier}_accountant',
                                                          name=f'{obj.name} Accountant', content_type=content_type)
        permission_auditor = Permission.objects.create(codename=f'tenant_{obj.identifier}_auditor',
                                                       name=f'{obj.name} Auditor',
                                                       content_type=content_type)

        # Create Group Objects and assign Permissions
        group = Group.objects.create(name=f'{obj.name} Administrators')
        group.permissions.add(permission_admin)
        group.permissions.add(permission_accountant)
        group.permissions.add(permission_auditor)

        group = Group.objects.create(name=f'{obj.name} Accountants')
        group.permissions.add(permission_accountant)
        group.permissions.add(permission_auditor)

        group = Group.objects.create(name=f'{obj.name} Auditors')
        group.permissions.add(permission_auditor)

    def delete_perms(self, obj):
        # Delete Groups
        Group.objects.get(name=f'{obj.name} Auditors').delete()
        Group.objects.get(name=f'{obj.name} Accountants').delete()
        Group.objects.get(name=f'{obj.name} Administrators').delete()

        # Delete Perms
        Permission.objects.get(codename=f'tenant_{obj.identifier}_admin').delete()
        Permission.objects.get(codename=f'tenant_{obj.identifier}_accountant').delete()
        Permission.objects.get(codename=f'tenant_{obj.identifier}_auditor').delete()


class CorporationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Corporation, CorporationAdmin)
