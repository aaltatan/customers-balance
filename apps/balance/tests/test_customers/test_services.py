from django.contrib.contenttypes.models import ContentType
from django.db.models import ProtectedError
from django.test import TestCase
from parameterized import parameterized

from apps.balance.forms import CustomerForm
from apps.balance.models import Customer
from apps.balance.services import add_customer, change_customer, delete_customer
from apps.core.models import Activity

from . import CustomersTestMixin


class TestServices(CustomersTestMixin, TestCase):
    @parameterized.expand(
        [
            ({"name": "Customer5"},),
            ({"name": "Customer6", "notes": "Amazing"},),
            (
                {
                    "name": "Customer7",
                    "mobile": "0947302503",
                    "notes": "Amazing",
                },
            ),
        ]
    )
    def test_add_service(self, data: dict[str, str]):
        form = CustomerForm(data=data)
        if form.is_valid():
            obj = add_customer(self.admin, form)

            activity_obj = Activity.objects.first()
            ct = ContentType.objects.get_for_model(Customer)

            self.assertEqual(data.get("name"), obj.name)
            self.assertEqual(data.get("mobile"), obj.mobile)
            self.assertEqual(data.get("notes", ""), obj.notes)

            self.assertEqual(Customer.objects.count(), 5)
            self.assertEqual(Activity.objects.count(), 1)

            self.assertEqual(activity_obj.kind, Activity.KindChoices.ADD)
            self.assertEqual(activity_obj.object_id, obj.pk)
            self.assertEqual(activity_obj.content_type, ct)
            self.assertEqual(activity_obj.user, self.admin)

    def test_delete_service(self):
        obj_pk = self.c4.pk
        delete_customer(self.admin, self.c4)

        activity_obj = Activity.objects.first()
        ct = ContentType.objects.get_for_model(Customer)

        self.assertEqual(Customer.objects.count(), 3)
        self.assertEqual(Activity.objects.count(), 1)

        self.assertEqual(activity_obj.kind, Activity.KindChoices.DELETE)
        self.assertEqual(activity_obj.object_id, obj_pk)
        self.assertEqual(activity_obj.content_type, ct)
        self.assertEqual(activity_obj.user, self.admin)
        self.assertEqual(
            activity_obj.data,
            {"name": "Customer4", "mobile": "0947302502", "notes": "Amazing"},
        )

    def test_delete_protected_object(self):
        with self.assertRaises(ProtectedError):
            delete_customer(self.admin, self.c1)

        self.assertEqual(Customer.objects.count(), 4)
        self.assertEqual(Activity.objects.count(), 0)

    def test_update_service(self):
        instance = Customer.objects.get(name="Customer1")
        form = CustomerForm(data={"name": "Abdullah"}, instance=instance)

        if form.is_valid():
            new_customer = change_customer(self.admin, instance, form)

            activity_obj = Activity.objects.first()
            ct = ContentType.objects.get_for_model(Customer)

            self.assertEqual(new_customer.name, "Abdullah")

            self.assertEqual(Customer.objects.count(), 4)
            self.assertEqual(Activity.objects.count(), 1)

            self.assertEqual(activity_obj.kind, Activity.KindChoices.CHANGE)
            self.assertEqual(activity_obj.object_id, instance.pk)
            self.assertEqual(activity_obj.content_type, ct)
            self.assertEqual(activity_obj.user, self.admin)
            self.assertEqual(
                activity_obj.data,
                {
                    "before": {"name": "Customer1"},
                    "after": {"name": "Abdullah"},
                },
            )

    def test_update_service_2(self):
        instance = Customer.objects.get(name="Customer1")
        form = CustomerForm(
            data={
                "name": "Abdullah",
                "mobile": "0955442233",
                "notes": "ss",
            },
            instance=instance,
        )

        if form.is_valid():
            new_customer = change_customer(self.admin, instance, form)

            activity_obj = Activity.objects.first()
            ct = ContentType.objects.get_for_model(Customer)

            self.assertEqual(new_customer.name, "Abdullah")

            self.assertEqual(Customer.objects.count(), 4)
            self.assertEqual(Activity.objects.count(), 1)

            self.assertEqual(activity_obj.kind, Activity.KindChoices.CHANGE)
            self.assertEqual(activity_obj.object_id, instance.pk)
            self.assertEqual(activity_obj.content_type, ct)
            self.assertEqual(activity_obj.user, self.admin)
            self.assertEqual(
                activity_obj.data,
                {
                    "before": {
                        "name": "Customer1",
                        "mobile": None,
                        "notes": "",
                    },
                    "after": {
                        "name": "Abdullah",
                        "mobile": "0955442233",
                        "notes": "ss",
                    },
                },
            )
