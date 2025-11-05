from datetime import datetime
from typing import Literal

from django.db import models
from django.db.models.functions import Coalesce
from django.utils import timezone

from apps.core.dbfields import MoneyField


def get_transactions_total_field(
    fieldname: Literal["debit", "credit", "amount"], query: models.Q
) -> Coalesce:
    return Coalesce(
        models.Sum(models.F(f"transactions__{fieldname}"), filter=query),
        0,
        output_field=MoneyField(),
    )


class CustomerQueryset(models.QuerySet):
    def annotate_totals(
        self,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> "CustomerQueryset":
        query = models.Q(transactions__is_deleted=False)

        if start_date:
            query &= models.Q(transactions__date__gte=start_date)
        if end_date:
            nearly_day = timezone.timedelta(hours=23, minutes=59, seconds=59)
            query &= models.Q(transactions__date__lte=end_date + nearly_day)

        return self.annotate(
            transactions_count=models.Count(
                models.F("transactions__debit"), filter=query
            ),
            total_debit=get_transactions_total_field("debit", query),
            total_credit=get_transactions_total_field("credit", query),
            net=get_transactions_total_field("amount", query),
        )

    def filter_date(
        self,
        *,
        start_date: timezone.datetime | None = None,
        end_date: timezone.datetime | None = None,
    ):
        return self.annotate_totals(
            start_date=start_date, end_date=end_date
        ).filter(~models.Q(transactions_count=0))

    def exclude_zero_net(self):
        return self.filter(~models.Q(net=0))


class CustomerManager(models.Manager):
    def get_queryset(self) -> CustomerQueryset:
        return CustomerQueryset(self.model, using=self._db)

    def annotate_totals(
        self,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> CustomerQueryset:
        return self.get_queryset().annotate_totals(
            start_date=start_date, end_date=end_date
        )

    def filter_date(
        self,
        *,
        start_date: timezone.datetime | None = None,
        end_date: timezone.datetime | None = None,
    ) -> CustomerQueryset:
        return self.get_queryset().filter_date(
            start_date=start_date, end_date=end_date
        )

    def exclude_zero_net(self):
        return self.get_queryset().exclude_zero_net()
