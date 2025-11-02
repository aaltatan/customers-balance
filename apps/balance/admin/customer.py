from decimal import Decimal

from django.contrib import admin
from django.http import HttpRequest

from apps.balance.models import Customer, Transaction
from apps.balance.services import add_customer, change_customer, delete_customer


class TransactionsInline(admin.TabularInline):
    model = Transaction
    extra = 0
    fields = ("date", "debit", "credit", "notes")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "transactions_count",
        "total_debit",
        "total_credit",
        "net",
        "mobile",
        "notes",
    )
    search_fields = ("name", "mobile", "notes")
    list_per_page = 10
    readonly_fields = ("slug", "created_at", "updated_at")
    fields = (
        ("created_at", "updated_at", "slug"),
        ("name", "mobile"),
        "notes",
    )
    inlines = (TransactionsInline,)

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate_totals()

    def save_model(self, request, obj, form, change):
        if change:
            change_customer(user=request.user, instance=obj, saver=form)
        else:
            add_customer(user=request.user, saver=form)

    def delete_model(self, request, obj):
        delete_customer(user=request.user, instance=obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            delete_customer(user=request.user, instance=obj)

    @admin.display(description="transactions count")
    def transactions_count(self, obj: Customer) -> str:
        return f"{obj.transactions_count:,}"

    @admin.display(description="total debit")
    def total_debit(self, obj: Customer) -> str:
        return f"{obj.total_debit:,}"

    @admin.display(description="total credit")
    def total_credit(self, obj: Customer) -> str:
        return f"{obj.total_credit:,}"

    @admin.display(description="net")
    def net(self, obj: Customer) -> str:
        return f"{obj.net:,}"
