from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = "title", "slug", "image", "total_likes", "created",
    list_filter = "created",
    prepopulated_fields = {"slug": ("title",)}
