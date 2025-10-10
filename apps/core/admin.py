from django.contrib import admin

from .models import Activity


@admin.register(Activity)
class ActivityManager(admin.ModelAdmin):
    list_display = (
        "kind",
        "user__username",
        "data",
        "content_object",
    )
    list_filter = ("user", "content_type")
    search_fields = ("object_id",)
