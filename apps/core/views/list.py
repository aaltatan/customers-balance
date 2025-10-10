from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import MultipleObjectMixin
from django_filters import FilterSet

from ..mixins import (
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

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        template_name = self.get_template_name()
        if request.htmx:
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

    def get_filterset(self, queryset: QuerySet) -> FilterSet:
        return self.filterset_class(self.request.GET, queryset, request=self.request)

    def get_search_filterset(self, queryset: QuerySet) -> FilterSet:
        SearchFilterset = self.get_search_filterset_class()
        return SearchFilterset(self.request.GET, queryset, request=self.request)

    def get_ordering_filterset(self, queryset: QuerySet) -> FilterSet:
        OrderingFilterset = self.get_ordering_filterset_class()
        return OrderingFilterset(self.request.GET, queryset, request=self.request)

    def get_template_name(self):
        app_label = self.get_app_label()
        model_name = self.get_model_name()
        return super().get_template_name(model_name, app_label)

    def get_partial_template_name(self):
        app_label = self.get_app_label()
        model_name = self.get_model_name()
        return super().get_partial_template_name(model_name, app_label)

    def get_context_data(self, **kwargs):
        context = {**kwargs}

        queryset = self.get_queryset()

        app_label = self.get_app_label()
        model_name = self.get_model_name()

        context.update(
            {
                "object_list": queryset,
                "container_id": f"{app_label}-{model_name}-container",
                "index_url": reverse_lazy(f"{app_label}:{model_name}:index"),
            }
        )

        if self.add_search_filterset:
            context["search_filterset"] = self.get_search_filterset(queryset)

        if self.add_ordering_filterset:
            context["ordering_filterset"] = self.get_ordering_filterset(queryset)

        if self.filterset_class:
            context["filterset"] = self.get_filterset(queryset)

        return context
