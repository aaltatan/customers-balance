from django import forms
from django.contrib import admin, messages
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.balance.managers import TransactionQueryset
from apps.balance.models import Transaction
from apps.balance.services import (
    add_transaction,
    change_transaction,
    delete_transaction,
    undelete_transaction,
)


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
    actions = ("undelete", "permanently_delete")
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

    def save_model(
        self,
        request: HttpRequest,
        obj: Transaction,
        form: forms.ModelForm,
        *,
        change: bool,
    ):
        if change:
            change_transaction(user=request.user, instance=obj, saver=form)
        else:
            add_transaction(user=request.user, saver=form)

    def delete_model(self, request: HttpRequest, obj: Transaction):
        delete_transaction(user=request.user, instance=obj)

    def delete_queryset(
        self, request: HttpRequest, queryset: TransactionQueryset
    ):
        for obj in queryset:
            delete_transaction(user=request.user, instance=obj)

    @admin.action(description=_("Undelete selected transactions"))
    def undelete(self, request: HttpRequest, queryset: TransactionQueryset):
        for obj in queryset:
            undelete_transaction(user=request.user, instance=obj)

        self.message_user(
            request,
            _("Selected transactions has been undeleted successfully"),
            level=messages.SUCCESS,
        )

    @admin.action(description=_("Delete PERMANENTLY selected transactions"))
    def permanently_delete(
        self, request: HttpRequest, queryset: TransactionQueryset
    ):
        for obj in queryset:
            delete_transaction(user=request.user, instance=obj, permanent=True)

        self.message_user(
            request,
            _("Selected transactions has been deleted permanently"),
            level=messages.SUCCESS,
        )

    @admin.display(description="debit")
    def formatted_debit(self, obj: Transaction):
        return f"{obj.debit:,}"

    @admin.display(description="credit")
    def formatted_credit(self, obj: Transaction):
        return f"{obj.credit:,}"
