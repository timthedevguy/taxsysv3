from django.contrib import admin
from django.urls import path
from .views import IndexView, SyncErrorView

urlpatterns = [
    path('', IndexView.as_view(), name="dashboard"),
    path('errors/sync', SyncErrorView.as_view(), name='sync-error')
]