from typing import Any, Protocol, TypeVar

from django.db import models

ModelType = TypeVar("ModelType", bound=models.Model)


class Saveable(Protocol[ModelType]):
    """a protocol presents either ModelForm or ModelSerializer instance"""

    def save(self, **kwargs: dict[str, Any]) -> ModelType:
        pass

    class Meta:
        model: type[models.Model]
