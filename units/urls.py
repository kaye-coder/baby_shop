from django.urls import path
from . import views

urlpatterns = [
    path('', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
]
