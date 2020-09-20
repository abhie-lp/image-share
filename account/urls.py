from django.urls import path, include

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("", include("django.contrib.auth.urls")),
    path("", views.dashboard, name="dashboard"),
]
