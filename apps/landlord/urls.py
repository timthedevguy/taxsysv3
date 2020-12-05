from django.urls import path, include
from . import views
from ..testauth.utils import TestOIDC

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('', views.IndexView.as_view(), name='landlord_index'),
    path('director/success/', views.DirectorSuccess.as_view(), name='landlord_director-success')
]