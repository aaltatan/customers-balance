from decimal import Decimal
from django.contrib import admin
from django.http import HttpRequest

from ..models import Customer, Transaction


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

    @admin.display(description="transactions count")
    def transactions_count(self, obj: Customer) -> str:
        transactions_count: Decimal = getattr(obj, "transactions_count")
        return f"{transactions_count:,}"

    @admin.display(description="total debit")
    def total_debit(self, obj: Customer) -> str:
        total_debit: Decimal = getattr(obj, "total_debit")
        return f"{total_debit:,}"

    @admin.display(description="total credit")
    def total_credit(self, obj: Customer) -> str:
        total_credit: Decimal = getattr(obj, "total_credit")
        return f"{total_credit:,}"

    @admin.display(description="net")
    def net(self, obj: Customer) -> str:
        net: Decimal = getattr(obj, "net")
        return f"{net:,}"
