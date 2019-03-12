from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import DashboardView

from . import views

urlpatterns = [
    path('', login_required(DashboardView.as_view()), name='dashboard'),
]