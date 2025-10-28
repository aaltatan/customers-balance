from typing import Protocol, TypeVar

from django.db import models


ModelType = TypeVar("ModelType", bound=models.Model)


class Saveable(Protocol[ModelType]):
    """ a protocol presents either ModelForm or ModelSerializer instance """
    def save(self, commit: bool = True) -> ModelType: ...
