from decimal import Decimal
from typing import Literal

from django.test import TestCase
from parameterized import parameterized

from apps.balance.filters import CustomerFilterset
from apps.balance.filters.customer import IncludeZeroNetChoices
from apps.balance.models import Customer, Transaction

from . import TestFiltersSetupMixin


class TestFilters(TestFiltersSetupMixin, TestCase):
    def test_model_has_right_counts(self):
        self.assertEqual(Customer.objects.count(), 4)
        self.assertEqual(Transaction.objects.count(), 11)

    def test_customers_has_right_net(self):
        expected = [
            Decimal("50_000"),  # Customer 1
            Decimal("90_000"),  # Customer 2
            Decimal("0"),  # Customer 3
            Decimal("0"),  # Customer 4
        ]
        for customer, expected_net in zip(self.init_qs, expected):
            self.assertEqual(customer.net, expected_net)

    def test_filterset_has_initial_exclude_zero_net(self):
        # initial request
        filtered_qs = CustomerFilterset(queryset=self.init_qs).qs
        self.assertEqual(filtered_qs.count(), 2)

    def test_filterset_has_initial_exclude_zero_net_with_data_obj(self):
        filtered_qs = CustomerFilterset(
            queryset=self.init_qs,
            data={"name": "Cus"},
        ).qs
        self.assertEqual(filtered_qs.count(), 4)

    def test_filterset_include_zero_nets(self):
        filtered_qs = CustomerFilterset(
            queryset=self.init_qs,
            data={
                "include_zero_nets": IncludeZeroNetChoices.YES,
            },
        ).qs
        self.assertEqual(filtered_qs.count(), 4)

    @parameterized.expand(
        [
            ("Customer 1", "Customer 1"),
            ("1 Customer", "Customer 1"),
            ("2", "Customer 2"),
            ("Cus 2", "Customer 2"),
            ("omer 3", "Customer 3"),
            ("Customer 4", "Customer 4"),
        ]
    )
    def test_filter_by_name(self, keyword: str, expected_name: str):
        filtered_qs = CustomerFilterset(
            queryset=self.init_qs, data={"name": keyword}
        ).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first().name, expected_name)

    @parameterized.expand(
        [
            ({"total_debit__gte": Decimal("100_000")}, ["Customer 1", "Customer 2"]),
            ({"total_credit__gte": Decimal("100_000")}, ["Customer 1", "Customer 2"]),
            ({"total_debit__lte": Decimal("100_000")}, ["Customer 3", "Customer 4"]),
            ({"net__lte": Decimal("0")}, ["Customer 3", "Customer 4"]),
            ({"net__gte": Decimal("51_000")}, ["Customer 2"]),
            ({"total_debit__lte": Decimal("10_000")}, ["Customer 4"]),
            ({"total_debit__gte": Decimal("500_000")}, []),
            ({"total_debit__lte": Decimal("-500_000")}, []),
            (
                {
                    "total_debit__gte": Decimal("20_000"),
                    "total_debit__lte": Decimal("200_000"),
                },
                ["Customer 1", "Customer 3"],
            ),
            (
                {
                    "total_debit__gte": Decimal("100_000"),
                    "total_credit__gte": Decimal("200_000"),
                },
                ["Customer 2"],
            ),
            (
                {
                    "net__lte": Decimal("50_000"),
                    "total_debit__gte": Decimal("150_000"),
                    "total_credit__gte": Decimal("150_000"),
                },
                ["Customer 1"],
            ),
        ]
    )
    def test_filter_by_totals_or_net(
        self, filters: dict[str, Decimal], expected_names: list[str]
    ):
        filters.update({"include_zero_nets": IncludeZeroNetChoices.YES})
        filtered_qs = CustomerFilterset(queryset=self.init_qs, data=filters).qs

        self.assertEqual(filtered_qs.count(), len(expected_names))
        self.assertEqual([customer.name for customer in filtered_qs], expected_names)

    @parameterized.expand(
        [
            ("gte", 3, ["Customer 1", "Customer 2", "Customer 3"]),
            ("gte", 2, ["Customer 1", "Customer 2", "Customer 3"]),
            ("lte", 0, ["Customer 4"]),
        ]
    )
    def test_filter_by_transactions_count(
        self, method: Literal["gte", "lte"], count: int, expected_names: list[str]
    ):
        filtered_qs = CustomerFilterset(
            queryset=self.init_qs, data={f"transactions_count__{method}": count}
        ).qs
        self.assertEqual(filtered_qs.count(), len(expected_names))
        self.assertEqual([customer.name for customer in filtered_qs], expected_names)

    def test_filter_by_date(self):
        pass
