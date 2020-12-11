from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from decorator_include import decorator_include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.testauth.account_urls')),
    path('oidc/', include('apps.testauth.oidc_urls')),
    re_path('(?P<tenant_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/',
            decorator_include(login_required, 'apps.tenant.urls')),
    path('', decorator_include(login_required, 'apps.tenant.accounts_urls')),
]
