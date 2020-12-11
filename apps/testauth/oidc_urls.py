from django.urls import path, include
from mozilla_django_oidc import urls
from . import views

# This combines the urls for MozillaOIDC and my custom ones for Director logins

base_urls = urls.urlpatterns

custom_urls = [
    path('authenticate/<str:token>/', views.DirectorOIDCAuthenticationRequestView.as_view(),
         name='director_oidc_authentication_init'),
    path('callback/<str:token>/', views.DirectorOIDCAuthenticationCallbackView.as_view(),
         name='director_oidc_authentication_callback')
]

urlpatterns = custom_urls + base_urls
