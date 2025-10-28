from django.db import models

from apps.core.dbfields import MoneyField


class TransactionQueryset(models.QuerySet):
    def annotate_net(self) -> "TransactionQueryset":
        return self.annotate(
            net=models.Window(
                expression=models.Sum(models.F("amount")),
                order_by=models.F("date").asc(),
                frame=models.RowRange(None, 0),
                output_field=MoneyField(),
            )
        )


class TransactionManager(models.Manager):
    def annotate_net(self) -> TransactionQueryset:
        return self.get_queryset().annotate_net()

    def get_queryset(self) -> TransactionQueryset:
        return (
            TransactionQueryset(self.model, using=self._db)
            .filter(is_deleted=False)
            .select_related("customer")
        )
