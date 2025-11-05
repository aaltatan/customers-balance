from django.db import models


class ModelInfoMixin:
    model: type[models.Model]

    def get_model_name(self) -> str:
        if self.model._meta is None:  # noqa: SLF001
            message = "you must define the model attribute."
            raise AttributeError(message)

        if self.model._meta.model_name is None:  # noqa: SLF001
            message = "you must define the model_name attribute."
            raise AttributeError(message)

        return self.model._meta.model_name  # noqa: SLF001

    def get_app_label(self) -> str:
        return self.model._meta.app_label  # noqa: SLF001
