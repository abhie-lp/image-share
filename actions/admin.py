from . import models
from django.contrib import admin


@admin.register(models.Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = "user", "verb", "target", "created",
    list_filter = "created",
    search_fields = "verb",
