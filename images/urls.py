from . import views
from django.urls import path

urlpatterns = [
    path("create/", views.image_create, name="image_create"),
]