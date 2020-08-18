from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
    path('errors/sync', views.SyncErrorView.as_view(), name='sync-error'),
    path('ajax/characters', views.ajax_get_alt_info, name='ajax-characters-info'),
]