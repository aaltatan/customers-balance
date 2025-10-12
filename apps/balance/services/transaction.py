from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from apps.core.models import User
from apps.core.models.activity import Activity
from apps.core.protocols import SaveableProtocol
from apps.core.services import Service

from ..models import Transaction, TransactionSerializer


class TransactionService(Service[Transaction]):
    model_class = Transaction


def add_transaction(user: User, saver: SaveableProtocol[Transaction]) -> Transaction:
    return TransactionService.add(user, saver)


def change_transaction(
    user: User,
    instance: Transaction,
    saver: SaveableProtocol[Transaction],
) -> Transaction:
    return TransactionService.change(
        user=user,
        instance=instance,
        serializer_class=TransactionSerializer,
        saver=saver,
    )


def delete_transaction(user: User, instance: Transaction) -> None:
    return TransactionService.delete(
        user, instance, serializer_class=TransactionSerializer
    )


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
