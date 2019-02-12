from . import views
from django.urls import path

urlpatterns = [
    path("create/", views.image_create, name="image_create"),
    path("like/", views.image_like, name="image_like"),
    path("ranking/", views.image_ranking, name="image_ranking"),
    path("detail/<int:id>/<slug:slug>/", views.image_detail, name="image_detail"),
    path("", views.image_list, name="image_list"),
]