from typing import Any

import django_filters as filters
from django import forms
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from .utils import annotate_search, get_keywords_query, parse_decimal


class FilterTextMixin:
    """A mixin that adds a text filter to a model."""

    def filter_text(self, qs: QuerySet, name: str, value: Any) -> QuerySet:
        if not value:
            return qs

        query = get_keywords_query(
            value,
            field_name=name,
        )
        return qs.filter(query)


class FilterStringDecimalMixin:
    def filter_string_decimal(self, qs: QuerySet, name: str, value: str) -> QuerySet:
        number = parse_decimal(value)
        return qs.filter(**{name: number})


class BaseQSearchFilter(filters.FilterSet):
    """a base class for filters that have a search field **(q)**."""

    search_fields: tuple[str, ...] = ()

    q = filters.CharFilter(
        method="search",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("search"),
            },
        ),
    )

    def search(
        self,
        queryset: QuerySet,
        _: str,
        value: str,
    ) -> QuerySet:
        """Search the queryset for the given name and value."""
        return queryset.annotate(search=annotate_search(*self.search_fields)).filter(get_keywords_query(value))


class CustomOrderingFilter(filters.OrderingFilter):
    descending_fmt = _("%s (desc)")


def get_ordering_filter(fields: dict[str, str]) -> CustomOrderingFilter:
    """Return an OrderingFilter."""
    return CustomOrderingFilter(fields=fields, field_labels=fields)


def get_decimal_range_filter(method_name: str = "filter_string_decimal"):
    from_ = filters.CharFilter(method=method_name)
    to = filters.CharFilter(method=method_name)
    return (from_, to)


def get_text_filter(method_name: str = "filter_text"):
    return filters.CharFilter(method=method_name)
