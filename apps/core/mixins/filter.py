import django_filters as filters
from django.db import models

from apps.core.filters import BaseQSearchFilter, get_ordering_filter


class SearchFilterMixin:
    model: models.Model
    search_filter_class: type[filters.FilterSet] | None = None
    search_fields: tuple[str, ...] | None = None

    def get_search_filterset_class(self):
        if getattr(self, "search_filter_class", None) and isinstance(self.search_filter_class, filters.FilterSet):
            return self.search_filter_class

        class SearchFilter(BaseQSearchFilter):
            search_fields = self.search_fields or ("id",)

            class Meta:
                model = self.model
                fields = ("id",)

        return SearchFilter


class OrderingFilterMixin:
    model: models.Model
    ordering_fields: dict[str, str] | None = None
    ordering_filter_class: type[filters.FilterSet] | None = None

    def get_ordering_filterset_class(self):
        if self.ordering_fields is None or len(self.ordering_fields) == 0:
            message = "you must define the ordering_fields attribute."
            raise AttributeError(message)

        if getattr(self, "ordering_filter_class", None) and isinstance(self.ordering_filter_class, filters.FilterSet):
            return self.ordering_filter_class

        class OrderingFilter(filters.FilterSet):
            ordering = get_ordering_filter(self.ordering_fields)

            class Meta:
                model = self.model
                fields = ("id",)

        return OrderingFilter
