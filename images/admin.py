from .models import Image
from django.contrib import admin


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = "id", "title", "total_likes", "user", "url", "created",
    list_display_links = "title",
    search_fields = "title", "user",
    prepopulated_fields = {"slug": ("title",)}
