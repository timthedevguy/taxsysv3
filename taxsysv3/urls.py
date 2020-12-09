"""taxsysv3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from decorator_include import decorator_include
from apps.testauth.views import DirectorOIDCAuthenticationCallbackView, DirectorOIDCAuthenticationRequestView


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('landlord/', decorator_include(login_required, 'apps.landlord.urls')),
    path('accounts/', include('apps.testauth.account_urls')),
    # path('accounts/profile/', decorator_include(login_required, 'apps.tenant.accounts_urls')),
    path('oidc/', include('apps.testauth.oidc_urls')),
    # path('sentry-debug/', trigger_error),
    re_path('(?P<tenant_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/',
            decorator_include(login_required, 'apps.tenant.urls')),
]
