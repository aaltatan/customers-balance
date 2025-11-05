import random

from apps.balance.models import Customer, Transaction


def run():
    customers_count = Customer.objects.count()
    for i in range(100):
        customer = Customer.objects.get(id=random.randint(1, customers_count))
        Transaction.objects.create(
            debit=random.randint(50_000, 100_000),
            customer=customer,
            notes=f"Notes {i}",
        )
        Transaction.objects.create(
            credit=random.randint(50_000, 100_000),
            customer=customer,
            notes=f"Notes {i}",
        )
