from django.contrib import admin
from .models import TestUser


class TestUserAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'username', 'auth_id', 'subject', 'is_staff', 'is_active')
    search_fields = (
        'display_name',
        'username'
    )


admin.site.register(TestUser, TestUserAdmin)
