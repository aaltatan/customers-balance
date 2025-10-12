from apps.core.models import User
from apps.core.protocols import SaveableProtocol
from apps.core.services import Service

from ..models import Customer, CustomerSerializer


class CustomerService(Service[Customer]):
    model_class = Customer


def add_customer(user: User, saver: SaveableProtocol[Customer]) -> Customer:
    return CustomerService.add(user, saver)


def change_customer(
    user: User,
    instance: Customer,
    saver: SaveableProtocol[Customer],
) -> Customer:
    return CustomerService.change(
        user=user,
        instance=instance,
        serializer_class=CustomerSerializer,
        saver=saver,
    )


def delete_customer(user: User, instance: Customer) -> None:
    return CustomerService.delete(user, instance, serializer_class=CustomerSerializer)
