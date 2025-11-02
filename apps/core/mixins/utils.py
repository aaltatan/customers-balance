from django.db import models


class ModelInfoMixin:
    model: type[models.Model]

    def get_model_name(self) -> str:
        if self.model._meta is None:
            raise AttributeError("you must define the model attribute.")

        if self.model._meta.model_name is None:
            raise AttributeError("you must define the model_name attribute.")

        return self.model._meta.model_name

    def get_app_label(self) -> str:
        return self.model._meta.app_label
