from typing import Any, ClassVar, Protocol

from django.db import models
from django.utils.text import slugify

from .utils import increase_slug_by_one


class SlugNameModelProtocol(Protocol):
    name: str
    slug: str
    pk: int

    objects: ClassVar[models.Manager]


def slugify_name(
    sender: Any,
    instance: SlugNameModelProtocol,
    *_: Any,
    **kwargs: dict[str, Any],
) -> None:
    slug: str | None = kwargs.get("slug")
    if slug is None:
        slug = slugify(instance.name, allow_unicode=True)

    model = instance.__class__

    slug_exists = (
        model.objects.filter(slug=slug).exclude(pk=instance.pk).exists()
    )

    if slug_exists:
        slug = increase_slug_by_one(slug)
        return slugify_name(
            sender=sender,
            instance=instance,
            slug=slug,
        )

    instance.slug = slug
    return None
