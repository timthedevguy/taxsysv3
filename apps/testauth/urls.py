from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('director/authenticate', views.DirectorOIDCAuthenticationRequestView.as_view(), name='director_oidc_authentication_init')
]