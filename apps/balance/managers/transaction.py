from django.db import models


class TransactionQueryset(models.QuerySet):
    pass


class TransactionManager(models.Manager):
    def get_queryset(self) -> TransactionQueryset:
        return (
            TransactionQueryset(self.model, using=self._db)
            .filter(is_deleted=False)
            .select_related("customer")
        )
