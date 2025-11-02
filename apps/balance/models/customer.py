from decimal import Decimal
from typing import Literal

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.balance.managers import CustomerManager
from apps.core.models import AbstractTimestampModel
from apps.core.signals import slugify_name
from apps.core.validators import four_char_validator, syrian_mobile_validator


class Customer(AbstractTimestampModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        unique=True,
        validators=[
            four_char_validator,
        ],
    )
    mobile = models.CharField(
        max_length=10,
        verbose_name=_("mobile"),
        default="",
        blank=True,
        validators=[
            syrian_mobile_validator,
        ],
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

    objects: CustomerManager = CustomerManager()

    def _get_total(self, field: Literal["debit", "credit"]) -> Decimal:
        return sum(getattr(transaction, field) for transaction in self.transactions.filter(is_deleted=False))

    def get_mobile_url(self):
        return f"tel:+963{self.mobile[1:]}" if self.mobile else "#"

    def get_total_debit(self) -> Decimal:
        return self._get_total("debit")

    def get_total_credit(self) -> Decimal:
        return self._get_total("credit")

    def get_net(self) -> Decimal:
        return self.get_total_debit() - self.get_total_credit()

    def get_transactions_count(self) -> int:
        return self.transactions.count()

    def get_absolute_url(self):
        return reverse("balance:customer:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ("name",)
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def __str__(self) -> str:
        return self.name


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("name", "mobile", "notes")


pre_save.connect(slugify_name, Customer)
