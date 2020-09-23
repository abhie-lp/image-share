from django.urls import path, include

from . import views

urlpatterns = [
    path("users/<str:username>/", views.user_detail, name="user_detail"),
    path("user/follow/", views.user_follow, name="user_follow"),
    path("users/", views.users_list, name="user_list"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("", include("django.contrib.auth.urls")),
    path("", views.dashboard, name="dashboard"),
]
