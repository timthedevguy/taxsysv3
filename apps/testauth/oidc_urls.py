from django.urls import path, include
from mozilla_django_oidc import urls
from . import views

base_urls = urls.urlpatterns

custom_urls = [
    path('authenticate/<str:tenant_id>/', views.DirectorOIDCAuthenticationRequestView.as_view(),
         name='director_oidc_authentication_init'),
    path('callback/<str:tenant_id>/', views.DirectorOIDCAuthenticationCallbackView.as_view(),
         name='director_oidc_authentication_callback')
]

urlpatterns = custom_urls + base_urls
