# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('create/', views.create_supplier, name='create_supplier'),
    path('update/<int:pk>/', views.update_supplier, name='update_supplier'),
    path('delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),  # URL for delete
]
