from django.contrib import admin, messages
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from ..models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "formatted_debit",
        "formatted_credit",
        "customer__name",
        "is_deleted",
        "notes",
    )
    list_display_links = ("date", "customer__name")
    search_fields = ("customer__name", "notes")
    list_per_page = 10
    list_filter = ("is_deleted",)
    actions = ("undelete",)
    readonly_fields = ("created_at", "updated_at", "slug")
    autocomplete_fields = ("customer",)
    fields = (
        ("created_at", "updated_at", "slug"),
        ("date", "notes"),
        ("debit", "credit", "customer"),
    )

    def get_queryset(self, request: HttpRequest):
        qs = Transaction.all_objects.all()

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)

        return qs

    @admin.action(description=_("Undelete selected transactions"))
    def undelete(self, request: HttpRequest, queryset: models.QuerySet):
        queryset.update(is_deleted=False)
        self.message_user(
            request,
            _("Selected transactions has been undeleted successfully"),
            level=messages.SUCCESS,
        )

    def delete_queryset(self, request: HttpRequest, queryset: models.QuerySet):
        queryset.update(is_deleted=True)

    @admin.display(description="debit")
    def formatted_debit(self, obj: Transaction):
        return f"{obj.debit:,}"

    @admin.display(description="credit")
    def formatted_credit(self, obj: Transaction):
        return f"{obj.credit:,}"
