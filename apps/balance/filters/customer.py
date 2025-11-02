from typing import Any

import django_filters as filters
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.balance.managers import CustomerQueryset
from apps.balance.models import Customer
from apps.core.filters import (
    FilterStringDecimalMixin,
    FilterTextMixin,
    get_decimal_range_filter,
    get_text_filter,
)


class IncludeZeroNetChoices(models.TextChoices):
    YES = "yes", _("Yes")
    NO = "no", _("No")


class CustomerFilterset(
    FilterStringDecimalMixin,
    FilterTextMixin,
    filters.FilterSet,
):
    name = get_text_filter()
    transactions_count__gte = filters.NumberFilter(field_name="transactions_count", lookup_expr="gte")
    transactions_count__lte = filters.NumberFilter(field_name="transactions_count", lookup_expr="lte")
    total_debit__gte, total_debit__lte = get_decimal_range_filter()
    total_credit__gte, total_credit__lte = get_decimal_range_filter()
    net__gte, net__lte = get_decimal_range_filter()
    date__gte = filters.CharFilter(method="filter_date")
    date__lte = filters.CharFilter(method="filter_date")
    include_zero_nets = filters.TypedChoiceFilter(
        method="filter_include_zero_nets",
        choices=IncludeZeroNetChoices.choices,
    )

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None) -> None:
        if not data:  # initial request
            data = {"include_zero_nets": IncludeZeroNetChoices.NO}
        super().__init__(data, queryset, request=request, prefix=prefix)

    def _parse_date(self, fieldname: str) -> timezone.datetime:
        date = self.form.cleaned_data.get(fieldname)

        if date:
            date = timezone.datetime.strptime(date, "%Y-%m-%d")

        return date

    def filter_date(self, qs: CustomerQueryset, _: str, __: dict[str, Any]) -> CustomerQueryset:
        try:
            start_date = self._parse_date("date__gte")
            end_date = self._parse_date("date__lte")
            return qs.filter_date(start_date=start_date, end_date=end_date)
        except ValueError:
            return qs.none()

    def filter_include_zero_nets(self, qs: CustomerQueryset, _: str, value: str) -> CustomerQueryset:
        if value == IncludeZeroNetChoices.NO:
            return qs.filter(~models.Q(net=0))

        return qs

    class Meta:
        model = Customer
        fields = ("name",)
