from django.urls import path, re_path

from . import views

urlpatterns = [
    #re_path(r'^ajax/types/search\?term=(?P<term>.*)&_type=query&q=.*$', views.type_name_search, name='evesde_type_name_search'),
    path('ajax/types/search', views.type_name_search, name='evesde_type_name_search'),
]