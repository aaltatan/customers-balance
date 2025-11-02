from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User


class ActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user", "content_type").prefetch_related("content_object")


class Activity(models.Model):
    class KindChoices(models.TextChoices):
        ADD = "add", _("add")
        CHANGE = "change", _("change")
        DELETE = "delete", _("delete")
        EXPORT = "export", _("export")
        OTHER = "other", _("other")

    created_at = models.DateTimeField(
        auto_now=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="activities",
    )
    kind = models.CharField(
        max_length=255,
        choices=KindChoices.choices,
        default=KindChoices.OTHER,
    )
    data = models.JSONField(
        null=True,
        blank=True,
    )
    notes = models.CharField(
        max_length=255,
        default="",
        blank=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    objects = ActivityManager()

    class Meta:
        ordering = ("-created_at", "kind")
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __str__(self) -> str:
        return f"Activity[{self.kind}] @{self.user.username}"
