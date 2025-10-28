from apps.core.models import User
from apps.core.protocols import Saveable
from apps.core.services import Service

from ..models import Customer, CustomerSerializer


class CustomerService(Service[Customer]):
    model_class = Customer


def add_customer(user: User, saver: Saveable[Customer]) -> Customer:
    return CustomerService.add(user, saver)


def change_customer(
    user: User, instance: Customer, saver: Saveable[Customer]
) -> Customer:
    return CustomerService.change(
        user=user,
        instance=instance,
        serializer_class=CustomerSerializer,
        saver=saver,
    )


def delete_customer(user: User, instance: Customer) -> None:
    return CustomerService.delete(user, instance, serializer_class=CustomerSerializer)
