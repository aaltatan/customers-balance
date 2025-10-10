from apps.core.models import User

from ...models import Customer, Transaction


class CustomersTestMixin:
    admin: User | None = None
    c1: Customer | None = None
    c2: Customer | None = None
    c3: Customer | None = None

    @classmethod
    def setUpTestData(cls):
        Customer(name="Customer1").save()
        Customer(name="Customer2", notes="Amazing").save()
        Customer(name="Customer3", notes="Amazing", mobile="0947302503").save()
        Customer(name="Customer4", notes="Amazing", mobile="0947302502").save()

        cls.c1 = Customer.objects.get(name="Customer1")
        cls.c2 = Customer.objects.get(name="Customer2")
        cls.c3 = Customer.objects.get(name="Customer3")
        cls.c4 = Customer.objects.get(name="Customer4")

        transactions = [
            # customer 1 = 0
            Transaction(debit=10_000, customer=cls.c1),
            Transaction(debit=20_000, customer=cls.c1),
            Transaction(credit=30_000, customer=cls.c1),
            # customer 2 = 75_000
            Transaction(debit=50_000, customer=cls.c2),
            Transaction(debit=50_000, customer=cls.c2),
            Transaction(credit=25_000, customer=cls.c2),
            # customer 3 = 65_000
            Transaction(debit=100_000, customer=cls.c3),
            Transaction(debit=50_000, customer=cls.c3),
            Transaction(credit=65_000, customer=cls.c3),
            Transaction(credit=20_000, customer=cls.c3),
        ]

        for trans in transactions:
            trans.save()

        cls.admin = User.objects.create_superuser(
            username="admin",
            password="admin",
        )

    @classmethod
    def tearDownClass(cls):
        Transaction.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.all().delete()
