from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Literal

from django.test import TestCase
from parameterized import parameterized

from apps.balance.filters import CustomerFilterset
from apps.balance.filters.customer import IncludeZeroNetChoices
from apps.balance.models import Customer, Transaction

from . import TestFiltersSetupMixin


@dataclass
class CustomerExpectedData:
    total_debit: Decimal
    total_credit: Decimal
    net: Decimal = field(init=False)

    def __post_init__(self) -> None:
        self.total_debit = Decimal(self.total_debit)
        self.total_credit = Decimal(self.total_credit)
        self.net = self.total_debit - self.total_credit


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
        filtered_qs = CustomerFilterset(queryset=self.init_qs, data={"name": keyword}).qs
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
    def test_filter_by_totals_or_net(self, filters: dict[str, Decimal], expected_names: list[str]):
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
    def test_filter_by_transactions_count(self, method: Literal["gte", "lte"], count: int, expected_names: list[str]):
        filtered_qs = CustomerFilterset(queryset=self.init_qs, data={f"transactions_count__{method}": count}).qs
        self.assertEqual(filtered_qs.count(), len(expected_names))
        self.assertEqual([customer.name for customer in filtered_qs], expected_names)

    @parameterized.expand(
        [
            (
                {
                    "date__lte": "2025-10-05",
                    "include_zero_nets": IncludeZeroNetChoices.NO,
                },
                {
                    "Customer 1": CustomerExpectedData(150_000, 0),
                    "Customer 2": CustomerExpectedData(450_000, 300_000),
                    "Customer 3": CustomerExpectedData(20_000, 0),
                },
            ),
            (
                {
                    "date__gte": "2025-10-05",
                    "date__lte": "2025-10-06",
                    "include_zero_nets": IncludeZeroNetChoices.NO,
                },
                {
                    "Customer 2": CustomerExpectedData(450_000, 400_000),
                    "Customer 3": CustomerExpectedData(20_000, 10_000),
                },
            ),
            (
                {
                    "date__gte": "2025-10-06",
                    "date__lte": "2025-10-07",
                    "include_zero_nets": IncludeZeroNetChoices.NO,
                },
                {
                    "Customer 1": CustomerExpectedData(50_000, 150_000),
                    "Customer 2": CustomerExpectedData(40_000, 100_000),
                    "Customer 3": CustomerExpectedData(0, 20_000),
                },
            ),
            (
                {
                    "date__gte": "2025-10-07",
                    "include_zero_nets": IncludeZeroNetChoices.NO,
                },
                {
                    "Customer 1": CustomerExpectedData(50_000, 0),
                    "Customer 2": CustomerExpectedData(40_000, 0),
                    "Customer 3": CustomerExpectedData(0, 10_000),
                },
            ),
        ]
    )
    def test_filter_by_date(self, data: dict[str, Any], customers: dict[str, CustomerExpectedData]):
        filtered_qs = CustomerFilterset(queryset=self.init_qs, data=data).qs

        self.assertEqual(filtered_qs.count(), len(customers))

        for (customer, expected_data), obj in zip(customers.items(), filtered_qs):
            self.assertEqual(customer, obj.name)
            self.assertEqual(obj.total_debit, expected_data.total_debit)
            self.assertEqual(obj.total_credit, expected_data.total_credit)
            self.assertEqual(obj.net, expected_data.net)
