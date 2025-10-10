from apps.core.models import User
from apps.core.protocols import SaverProtocol
from apps.core.services import Service

from ..models import Transaction, TransactionSerializer


class TransactionService(Service[Transaction]):
    model_class = Transaction


def add_transaction(user: User, saver: SaverProtocol[Transaction]) -> Transaction:
    return TransactionService.add(user, saver)


def change_transaction(
    user: User,
    instance: Transaction,
    saver: SaverProtocol[Transaction],
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
