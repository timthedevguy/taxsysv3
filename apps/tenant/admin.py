from django.contrib import admin
from .models import Tenant

# Register your models here.
class TenantAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tenant, TenantAdmin)