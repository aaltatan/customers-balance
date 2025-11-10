from django import forms
from django.db import models


class ModelInfoMixin:
    model: type[models.Model] | None = None
    form_class: type[forms.ModelForm] | None = None

    def get_model_class(self) -> type[models.Model]:
        if self.model is not None:
            return self.model

        if (
            self.form_class is not None
            and self.form_class._meta.model is not None  # noqa: SLF001
        ):
            return self.form_class._meta.model  # noqa: SLF001

        message = "you must define the model or form_class attribute."
        raise AttributeError(message)

    def get_model_name(self) -> str:
        model = self.get_model_class()

        if model._meta is None:  # noqa: SLF001
            message = "you must define the model attribute."
            raise AttributeError(message)

        if model._meta.model_name is None:  # noqa: SLF001
            message = "you must define the model_name attribute."
            raise AttributeError(message)

        return model._meta.model_name  # noqa: SLF001

    def get_app_label(self) -> str:
        model = self.get_model_class()
        return model._meta.app_label  # noqa: SLF001
