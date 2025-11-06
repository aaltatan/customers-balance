from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractTimestampModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )

    class Meta:
        abstract = True


class AbstractSoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("is deleted"),
    )

    class Meta:
        abstract = True

    def undelete(self):
        self.is_deleted = False
        self.save()

    def delete(
        self,
        using: Any = None,
        *,
        keep_parents: bool = False,
        permanent: bool = False,
    ):
        if permanent:
            super().delete(using=using, keep_parents=keep_parents)
        else:
            self.is_deleted = True
            self.save()
