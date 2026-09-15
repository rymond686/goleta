from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import RateLimitedLoginView, register

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", RateLimitedLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
