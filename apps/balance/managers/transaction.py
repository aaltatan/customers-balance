from django.db import models

from apps.core.dbfields import MoneyField


class TransactionQueryset(models.QuerySet):
    def annotate_net(self) -> "TransactionQueryset":
        return self.annotate(
            net=models.Window(
                expression=models.Sum(
                    "amount", filter=models.Q(is_deleted=False)
                ),
                frame=models.RowRange(None, 0),
                order_by=(
                    models.F("date").asc(),
                    models.F("customer__name").asc(),
                ),
                output_field=MoneyField(),
            )
        )


class TransactionManager(models.Manager):
    def annotate_net(self) -> TransactionQueryset:
        return self.get_queryset().annotate_net()

    def get_queryset(self) -> TransactionQueryset:
        return (
            TransactionQueryset(self.model, using=self._db)
            .select_related("customer")
            .order_by(models.F("date").desc(), models.F("customer__name").asc())
        )
