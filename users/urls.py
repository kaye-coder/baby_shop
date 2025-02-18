# users/urls.py

from django.urls import path
from .views import login_view, logout_view, dashboard, add_user, user_list, user_detail

urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("add-user/", add_user, name="add_user"),
    path("user-list/", user_list, name="user_list"),
    path("user-detail/<int:user_id>/", user_detail, name="user_detail"),
]
