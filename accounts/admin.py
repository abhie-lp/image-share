from . import models
from django.contrib import admin


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "id", "user", "photo",
    list_filter = "date_of_birth",
    list_display_links = "id", "user",
    search_fields = "user",