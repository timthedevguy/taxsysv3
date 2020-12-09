from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/<str:token>/', views.DirectorLoginView.as_view(), name='director_login')
]