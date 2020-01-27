from django.contrib import admin
from .models import TestUser


class TestUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'auth_id', 'subject', 'is_staff', 'is_active')

admin.site.register(TestUser, TestUserAdmin)
