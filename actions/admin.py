from django.contrib import admin
from actions.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = "user", "verb", "target", \
                   "target_ct", "target_id", "created"
