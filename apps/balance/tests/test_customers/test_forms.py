from django.test import TestCase
from parameterized import parameterized

from apps.balance.forms import CustomerForm
from apps.balance.models import Customer

from . import CustomersTestMixin


class TestModels(CustomersTestMixin, TestCase):
    def test_model_objects(self):
        self.assertEqual(Customer.objects.count(), 4)

    @parameterized.expand(
        [
            ({"name": "Customer5"},),
            ({"name": "Customer6", "mobile": "0947302503"},),
            ({"name": "Customer7", "mobile": "0947302503", "notes": "3123"},),
        ]
    )
    def test_create_with_valid_data(self, data: dict[str, str]):
        form = CustomerForm(data=data)
        if form.is_valid():
            form.save()

        self.assertEqual(Customer.objects.count(), 5)

    def test_update_with_valid_data(self):
        instance = Customer.objects.get(name="Customer1")
        data = {"name": "Customer1", "mobile": "0966346546", "notes": "google"}
        form = CustomerForm(data=data, instance=instance)
        if form.is_valid():
            obj = form.save()

            self.assertEqual(obj.name, data["name"])
            self.assertEqual(obj.mobile, data["mobile"])
            self.assertEqual(obj.notes, data["notes"])

    def test_update_with_invalid_data(self):
        instance = Customer.objects.get(name="Customer1")
        data = {"name": "Customer1", "mobile": "0966346", "notes": "google"}
        form = CustomerForm(data=data, instance=instance)

        self.assertFalse(form.is_valid())
        self.assertIn("mobile", form.errors)
        self.assertIn(
            "mobile number's pattern must be like 0933222111",
            form.errors["mobile"],
        )

    def test_update_with_duplicated_name(self):
        instance = Customer.objects.get(name="Customer2")
        data = {"name": "Customer1", "mobile": "0966346546", "notes": "google"}
        form = CustomerForm(data=data, instance=instance)

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn(
            "Customer with this Name already exists.", form.errors["name"]
        )

    def test_create_with_duplicated_name(self):
        data = {"name": "Customer1"}
        form = CustomerForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn(
            "Customer with this Name already exists.", form.errors["name"]
        )

    def test_name_less_than_four_chars(self):
        data = {"name": "Aaa"}
        form = CustomerForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn(
            "field must be 4 characters at least", form.errors["name"]
        )

    @parameterized.expand([("09445522",), ("5544552233",), ("094455223",)])
    def test_invalid_mobile_pattern(self, mobile: str):
        data = {"name": "Unique Name", "mobile": mobile}
        form = CustomerForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("mobile", form.errors)
        self.assertIn(
            "mobile number's pattern must be like 0933222111",
            form.errors["mobile"],
        )
