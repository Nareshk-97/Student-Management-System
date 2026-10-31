from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    AccountLoginView,
    login_success,
    admin_dashboard,
    register,
)

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", AccountLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login-success/", login_success, name="login_success"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
]