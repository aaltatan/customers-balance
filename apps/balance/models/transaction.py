import uuid
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core.dbfields import MoneyField
from apps.core.models import AbstractSoftDeleteModel, AbstractTimestampModel

from .customer import Customer


class TransactionQueryset(models.QuerySet):
    pass


class TransactionManager(models.Manager):
    def get_queryset(self):
        return (
            TransactionQueryset(self.model, using=self._db)
            .filter(is_deleted=False)
            .select_related("customer")
        )


class Transaction(AbstractTimestampModel, AbstractSoftDeleteModel):
    uuid = models.UUIDField(
        verbose_name="uuid",
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    date = models.DateTimeField(
        verbose_name=_("date"),
        default=timezone.now,
    )
    debit = MoneyField(
        verbose_name=_("debit"),
        default=0,
    )
    credit = MoneyField(
        verbose_name=_("credit"),
        default=0,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        verbose_name=_("customer"),
        related_name="transactions",
    )
    notes = models.TextField(
        verbose_name=_("notes"),
        default="",
        blank=True,
    )
    slug = models.SlugField(
        verbose_name=_("slug"),
        unique=True,
        null=True,
        blank=True,
        default=None,
        allow_unicode=True,
    )

    objects: TransactionManager = TransactionManager()
    all_objects: models.Manager = models.Manager()

    def clean(self):
        errors: dict[str, ValidationError] = {}

        if self.debit == 0 and self.credit == 0:
            errors["debit"] = ValidationError(
                _("both debit and credit cannot be zero.")
            )
            errors["credit"] = ValidationError(
                _("both debit and credit cannot be zero.")
            )

        if self.debit != 0 and self.credit != 0:
            errors["debit"] = ValidationError(
                _("both debit and credit cannot be filled.")
            )
            errors["credit"] = ValidationError(
                _("both debit and credit cannot be filled.")
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return f"{self.customer.name}(debit={self.debit:,}, credit={self.credit:,})"

    class Meta:
        ordering = ("date",)
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")


class TransactionSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()

    def get_customer_name(self, obj: Transaction) -> str:
        return obj.customer.name

    class Meta:
        model = Transaction
        fields = ("date", "debit", "credit", "customer_name", "notes")


def slugify_transaction(
    sender: Any,
    instance: Transaction,
    *args,
    **kwargs: dict[str, Any],
) -> None:
    if instance.slug is None:
        instance.slug = instance.uuid.hex


pre_save.connect(slugify_transaction, Transaction)
