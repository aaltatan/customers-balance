from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from apps.balance.models import Transaction, TransactionSerializer
from apps.core.models import User
from apps.core.models.activity import Activity
from apps.core.protocols import Saveable
from apps.core.services import add_instance, change_instance


def add_transaction(user: User, saver: Saveable[Transaction]) -> Transaction:
    return add_instance(user, saver)


def change_transaction(
    user: User, instance: Transaction, saver: Saveable[Transaction]
) -> Transaction:
    return change_instance(
        user=user,
        instance=instance,
        serializer_class=TransactionSerializer,
        saver=saver,
    )


@transaction.atomic
def delete_transaction(
    user: User, instance: Transaction, *, permanent: bool = False
) -> None:
    data = TransactionSerializer(instance).data
    instance_pk = instance.pk

    instance.delete(permanent=permanent)

    Activity(
        user=user,
        kind=Activity.KindChoices.DELETE,
        object_id=instance_pk,
        data=data,
        content_type=ContentType.objects.get_for_model(Transaction),
        notes="DELETE PERMANENTLY" if permanent else "DELETE",
    ).save()


@transaction.atomic
def undelete_transaction(user: User, instance: Transaction) -> None:
    instance.undelete()
    Activity.objects.create(
        user=user,
        kind=Activity.KindChoices.OTHER,
        object_id=instance.pk,
        content_type=ContentType.objects.get_for_model(Transaction),
        notes="UNDELETE",
    )
