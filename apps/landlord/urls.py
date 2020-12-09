from django.urls import path, include
from . import views
from ..testauth.utils import TestOIDC

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('', views.IndexView.as_view(), name='landlord_index'),
    # path('director/success/<str:tenant_id>/', views.DirectorSuccess.as_view(), name='landlord_director_success'),
    # path('director/characters/', views.ajax_get_characters, name='ajax_director_get_characters'),
    # path('director/character/', views.ajax_get_character_info, name='ajax_director_get_character'),
    # path('director/character/<int:character_id>/', views.ajax_get_character_info, name='ajax_director_get_character')
]