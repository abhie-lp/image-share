from django.urls import path
from . import views

app_name = "images"

urlpatterns = [
    path("detail/<int:pk>/<slug:slug>/", views.image_detail, name="detail"),
    path("sort/<str:sort>/", views.image_list, name="list_sort"),
    path("ranking/", views.image_ranking, name="ranking"),
    path("like/", views.image_like, name="like"),
    path("create/", views.image_create, name="create"),
    path("", views.image_list, name="list"),
]
