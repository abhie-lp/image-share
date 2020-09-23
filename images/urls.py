from django.urls import path
from . import views

app_name = "images"

urlpatterns = [
    path("detail/<int:pk>/<slug:slug>/", views.image_detail, name="detail"),
    path("create/", views.image_create, name="create"),
]
