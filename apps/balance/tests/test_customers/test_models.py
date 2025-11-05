from decimal import Decimal

from django.db.utils import IntegrityError
from django.test import TestCase
from parameterized import parameterized

from apps.balance.models import Customer

from . import CustomersTestMixin


class TestModels(CustomersTestMixin, TestCase):
    def test_model_objects(self):
        self.assertEqual(Customer.objects.count(), 4)

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Customer(name="Customer1").save()

    def test_delete_protected_object(self):
        with self.assertRaises(IntegrityError):
            self.c1.delete()

    @parameterized.expand(
        [
            ("Customer1", Decimal(30000), Decimal(30000), Decimal(0), 3),
            (
                "Customer2",
                Decimal(100000),
                Decimal(25000),
                Decimal(75000),
                3,
            ),
            (
                "Customer3",
                Decimal(150000),
                Decimal(85000),
                Decimal(65000),
                4,
            ),
        ]
    )
    def test_totals(
        self,
        name: str,
        total_debit: Decimal,
        total_credit: Decimal,
        net: Decimal,
        transactions_count: int,
    ):
        instance = Customer.objects.get(name=name)

        self.assertEqual(total_debit, instance.get_total_debit())
        self.assertEqual(total_credit, instance.get_total_credit())
        self.assertEqual(net, instance.get_net())
        self.assertEqual(transactions_count, instance.get_transactions_count())

    def test_annotate_totals(self):
        qs = Customer.objects.annotate_totals().order_by("name").all()
        data = [
            (Decimal(30000), Decimal(30000), Decimal(0), 3),
            (Decimal(100000), Decimal(25000), Decimal(75000), 3),
            (Decimal(150000), Decimal(85000), Decimal(65000), 4),
        ]

        for row in zip(qs, data, strict=False):
            customer, expected = row
            total_debit, total_credit, net, transactions_count = expected
            self.assertEqual(customer.total_debit, total_debit)
            self.assertEqual(customer.total_credit, total_credit)
            self.assertEqual(customer.net, net)
            self.assertEqual(customer.transactions_count, transactions_count)
