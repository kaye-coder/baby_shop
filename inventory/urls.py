# urls.py
from django.urls import path
from .views import inventory_list, add_inventory, update_inventory, delete_inventory_item

urlpatterns = [
    path('', inventory_list, name='inventory_list'),
    path('add/', add_inventory, name='add_inventory'),
    path('update/<int:pk>/', update_inventory, name='update_inventory'),
    path('delete/<int:item_id>/', delete_inventory_item, name='delete_inventory'),
]
