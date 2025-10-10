import django_filters as filters
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    FilterStringDecimalMixin,
    FilterTextMixin,
    get_decimal_range_filter,
    get_text_filter,
)

from ..managers import CustomerQueryset
from ..models import Customer


class IncludeZeroNetChoices(models.TextChoices):
    YES = "yes", _("Yes")
    NO = "no", _("No")


class CustomerFilterset(
    FilterStringDecimalMixin,
    FilterTextMixin,
    filters.FilterSet,
):
    name = get_text_filter()
    transactions_count__gte = filters.NumberFilter(
        field_name="transactions_count", lookup_expr="gte"
    )
    transactions_count__lte = filters.NumberFilter(
        field_name="transactions_count", lookup_expr="lte"
    )
    total_debit__gte, total_debit__lte = get_decimal_range_filter()
    total_credit__gte, total_credit__lte = get_decimal_range_filter()
    net__gte, net__lte = get_decimal_range_filter()
    date__gte = filters.CharFilter(method="filter_date__gte")
    date__lte = filters.CharFilter(method="filter_date__lte")
    include_zero_nets = filters.TypedChoiceFilter(
        method="filter_include_zero_nets",
        choices=IncludeZeroNetChoices.choices,
    )

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        if not data:  # initial request
            data = {"include_zero_nets": IncludeZeroNetChoices.NO}
        super().__init__(data, queryset, request=request, prefix=prefix)

    def filter_date__gte(
        self, qs: CustomerQueryset, name: str, value: timezone.datetime
    ) -> CustomerQueryset:
        try:
            start_date = timezone.datetime.strptime(value, "%Y-%m-%d")
            return qs.filter_date(start_date=start_date)
        except ValueError:
            return qs.none()

    def filter_date__lte(
        self, qs: CustomerQueryset, name: str, value: str
    ) -> CustomerQueryset:
        try:
            end_date = timezone.datetime.strptime(value, "%Y-%m-%d")
            return qs.filter_date(end_date=end_date)
        except ValueError:
            return qs.none()

    def filter_include_zero_nets(
        self, qs: CustomerQueryset, name: str, value: str
    ) -> CustomerQueryset:
        if value == IncludeZeroNetChoices.NO:
            return qs.filter(~models.Q(net=0))

        return qs

    class Meta:
        model = Customer
        fields = ("name",)
