from django.contrib import admin
from django.urls import path
from . import views
from . import ajax

urlpatterns = [
    path('', views.TenantIndex.as_view(), name='tenant_index'),
    path('errors/sync', views.SyncErrorView.as_view(), name='sync-error'),
    path('ajax/characters', views.ajax_get_alt_info, name='ajax-characters-info'),
    path('director/success/', views.DirectorSuccess.as_view(), name='landlord_director_success'),
    path('director/characters/', views.ajax_get_characters, name='ajax_director_get_characters'),
    path('director/character/', views.ajax_get_character_info, name='ajax_director_get_character'),
    path('director/character/<int:character_id>/', views.ajax_get_character_info, name='ajax_director_get_character'),
    path('director/test/', views.ajax_test, name='ajax_test'),
    path('admin/', views.TenantAdminIndex.as_view(), name='tenant_admin'),
    path('ajax/director/count/', ajax.ajax_get_director_char_count, name='ajax_director_get_count')
]