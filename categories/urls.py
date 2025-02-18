from django.urls import path
from .views import (
    category_list, semi_category_list, add_category, add_semi_category, delete_category, delete_semi_category
)

urlpatterns = [
    path("", category_list, name="category_list"),
    path("semi-categories/", semi_category_list, name="semi_category_list"),
    path("add/", add_category, name="add_category"),
    path("semi-categories/add/", add_semi_category, name="add_semi_category"),
    path("categories/delete/<int:pk>/", delete_category, name="delete_category"),
    path("semi-categories/delete/<int:pk>/", delete_semi_category, name="delete_semi_category"),
]
