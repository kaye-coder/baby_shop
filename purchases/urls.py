from django.urls import path
from .views import create_purchase, purchase_list, delete_purchase

urlpatterns = [
    path('create/', create_purchase, name='create_purchase'),
    path('', purchase_list, name='purchase_list'),
    path('delete/<int:pk>/', delete_purchase, name='delete_purchase'),
]
