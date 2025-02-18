# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_list, name='sales_list'),
    path('sales/create/', views.sales_create, name='sales_create'),
    path('sales/receipt/<int:sale_id>/', views.sales_receipt, name='sales_receipt'),
    path('sales/update_payment/<int:sale_id>/', views.update_payment, name='update_payment'),
    path('sales/delete/<int:sale_id>/', views.sales_delete, name='sales_delete'),  # Ensure this pattern is present
]
