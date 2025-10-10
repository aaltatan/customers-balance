from django.db import models


class ModelInfoMixin:
    model: type[models.Model]

    def get_model_name(self) -> str:
        return self.model._meta.model_name

    def get_app_label(self) -> str:
        return self.model._meta.app_label
