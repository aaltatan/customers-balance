from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Activity, User

admin.site.register(User, UserAdmin)


@admin.register(Activity)
class ActivityManager(admin.ModelAdmin):
    list_display = (
        "kind",
        "user__username",
        "data",
        "content_object",
        "notes",
    )
    list_filter = ("user", "content_type")
    search_fields = ("object_id",)
    readonly_fields = (
        "user",
        "kind",
        "object_id",
        "data",
        "content_type",
        "notes",
    )
