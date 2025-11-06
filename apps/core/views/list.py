from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import MultipleObjectMixin
from django_filters import FilterSet

from apps.core.mixins import (
    ModelInfoMixin,
    OrderingFilterMixin,
    SearchFilterMixin,
    TemplateListMixin,
)


class ListView(
    ModelInfoMixin,
    TemplateListMixin,
    OrderingFilterMixin,
    SearchFilterMixin,
    MultipleObjectMixin,
    View,
):
    filterset_class: type[FilterSet] | None = None
    paginate_by = 10
    add_search_filterset: bool = True
    add_ordering_filterset: bool = True

    def get(
        self, request: HttpRequest, *_: Any, **__: dict[str, Any]
    ) -> HttpResponse:
        template_name = self.get_template_name()
        if getattr(request, "htmx", False):
            template_name = self.get_partial_template_name()

        context = self.get_context_data()

        return render(request, template_name, context)

    def get_initial_queryset(self):
        return self.model.objects.all()

    def get_queryset(self):
        queryset = self.get_initial_queryset()

        if self.add_search_filterset:
            queryset = self.get_search_filterset(queryset).qs

        if self.add_ordering_filterset:
            queryset = self.get_ordering_filterset(queryset).qs

        if self.filterset_class:
            queryset = self.get_filterset(queryset).qs

        return queryset

    def paginate_queryset(self, queryset: QuerySet, page_size: int):
        return super().paginate_queryset(queryset, page_size)

    def get_filterset(self, queryset: QuerySet) -> FilterSet:
        if self.filterset_class is None:
            message = "you must define the filterset_class attribute."
            raise AttributeError(message)

        return self.filterset_class(
            self.request.GET, queryset, request=self.request
        )

    def get_search_filterset(self, queryset: QuerySet) -> FilterSet:
        filterset = self.get_search_filterset_class()
        return filterset(self.request.GET, queryset, request=self.request)

    def get_ordering_filterset(self, queryset: QuerySet) -> FilterSet:
        filterset = self.get_ordering_filterset_class()
        return filterset(self.request.GET, queryset, request=self.request)

    def get_template_name(self):
        app_label = self.get_app_label()
        model_name = self.get_model_name()
        return super().get_template_name(model_name, app_label)

    def get_partial_template_name(self):
        app_label = self.get_app_label()
        model_name = self.get_model_name()
        return super().get_partial_template_name(model_name, app_label)

    def get_page_size(self):
        if not getattr(self, "page_size", None) and not isinstance(
            self.paginate_by, int
        ):
            message = "you must define the page_size attribute."
            raise AttributeError(message)

        return self.paginate_by

    def get_context_data(self, **kwargs: dict[str, Any]):
        context = {**kwargs}

        queryset = self.get_queryset()

        page_size = self.get_page_size()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size
        )

        app_label = self.get_app_label()
        model_name = self.get_model_name()

        context.update(
            {
                "paginator": paginator,
                "page_obj": page,
                "is_paginated": is_paginated,
                "object_list": queryset,
                "container_id": f"{app_label}-{model_name}-container",
                "index_url": reverse_lazy(f"{app_label}:{model_name}:index"),
            },
        )

        if self.add_search_filterset:
            context["search_filterset"] = self.get_search_filterset(queryset)
            context["search_filterset_form_id"] = (
                f"{app_label}-{model_name}-search-form"
            )

        if self.add_ordering_filterset:
            context["ordering_filterset"] = self.get_ordering_filterset(
                queryset
            )

        if self.filterset_class:
            context["filterset"] = self.get_filterset(queryset)

        return context
