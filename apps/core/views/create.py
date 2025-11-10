from typing import Any

from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from apps.core.mixins import ModelInfoMixin, TemplateCreateMixin


class CreateView(ModelInfoMixin, TemplateCreateMixin, View):
    form_class: type[forms.ModelForm]
    create_url: str | None = None
    initial: dict[str, Any] | None = None

    def get(self, request: HttpRequest, *_: Any, **__: Any) -> HttpResponse:
        template_name = self.get_template_name()
        is_request_htmx = getattr(request, "htmx", False)

        if is_request_htmx:
            template_name = self.get_partial_template_name()

        context = self.get_context_data()

        response = render(request, template_name, context)

        if is_request_htmx:
            response["HX-Trigger"] = "showmodal"

        return response

    def get_initial(self):
        if self.initial is not None and isinstance(self.initial, dict):
            return self.initial

        return {}

    def get_create_url(self):
        if self.create_url is not None and isinstance(self.create_url, str):
            return self.create_url

        app_label = self.get_app_label()
        model_name = self.get_model_name()
        return reverse(f"{app_label}:{model_name}:create")

    def get_template_name(self) -> str:
        model_name = self.get_model_name()
        app_label = self.get_app_label()
        return super().get_template_name(model_name, app_label)

    def get_partial_template_name(self) -> str:
        model_name = self.get_model_name()
        app_label = self.get_app_label()
        return super().get_partial_template_name(model_name, app_label)

    def get_context_data(self, **kwargs: Any):
        form_kwargs = {
            "data": self.request.POST or None,
            "files": self.request.FILES or None,
        }

        initial = self.get_initial()

        if initial:
            form_kwargs["initial"] = initial

        form = self.form_class(**form_kwargs)
        create_url = self.get_create_url()

        return {"form": form, "create_url": create_url, **kwargs}
