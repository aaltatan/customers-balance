from apps.balance.models import Customer, CustomerSerializer
from apps.core.models import User
from apps.core.protocols import Saveable
from apps.core.services import add_instance, change_instance, delete_instance


def add_customer(user: User, saver: Saveable[Customer]) -> Customer:
    return add_instance(user, saver)


def change_customer(
    user: User, instance: Customer, saver: Saveable[Customer]
) -> Customer:
    return change_instance(
        user=user,
        instance=instance,
        serializer_class=CustomerSerializer,
        saver=saver,
    )


def delete_customer(user: User, instance: Customer) -> None:
    return delete_instance(user, instance, serializer_class=CustomerSerializer)
