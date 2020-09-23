from django.urls import path
from . import views

app_name = "images"

urlpatterns = [
    path("detail/<int:pk>/<slug:slug>/", views.image_detail, name="detail"),
    path("like/", views.image_like, name="like"),
    path("create/", views.image_create, name="create"),
    path("", views.image_list, name="list"),
]
