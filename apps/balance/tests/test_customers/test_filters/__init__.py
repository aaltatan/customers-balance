from django.utils.timezone import datetime

from ....models import Customer, Transaction


class TestFiltersSetupMixin:
    @classmethod
    def setUpTestData(cls):
        Customer(name="Customer 1").save()
        Customer(name="Customer 2", notes="Amazing").save()
        Customer(name="Customer 3", notes="Amazing", mobile="0947302503").save()
        Customer(name="Customer 4", notes="Amazing", mobile="0947302502").save()

        cls.c1 = Customer.objects.get(name="Customer 1")
        cls.c2 = Customer.objects.get(name="Customer 2")
        cls.c3 = Customer.objects.get(name="Customer 3")
        cls.c4 = Customer.objects.get(name="Customer 4")

        cls.init_qs = Customer.objects.annotate_totals().order_by("name").all()

        # data
        # ---------------------------------------------
        # date	      customer	  debit 	    credit
        # ---------------------------------------------
        #! 2025-10-05	c1	        100,000 	-
        #! 2025-10-05	c1	        50,000 	    -
        #? 2025-10-05	c2	        450,000 	-
        #? 2025-10-05	c2	        -   	    300,000
        #* 2025-10-05	c3	        20,000 	    -

        #! 2025-10-06	c1	        -   	    150,000
        #? 2025-10-06	c2	        -   	    100,000
        #* 2025-10-06	c3	        -   	    10,000

        #! 2025-10-07	c1	        50,000 	    -
        #? 2025-10-07	c2	        40,000 	    -
        #* 2025-10-07	c3	        -   	    10,000

        # pivot report
        # ---------------------------------------------------------------------
        # Row Labels	  c1	        c2	        c3 	        c4    Total
        # ---------------------------------------------------------------------
        # 2025-10-05	  150,000 	    150,000 	20,000 	    -     320,000
        # 2025-10-06	  (150,000)	    (100,000)	(10,000)	-     (260,000)
        # 2025-10-07	  50,000 	    40,000 	    (10,000)	-     80,000
        # ---------------------------------------------------------------------
        # Grand Total	  50,000 	    90,000 	    -   	    -     140,000

        transactions = [
            Transaction(debit=100_000, customer=cls.c1, date=datetime(2025, 10, 5)),
            Transaction(debit=50_000, customer=cls.c1, date=datetime(2025, 10, 5)),
            Transaction(debit=450_000, customer=cls.c2, date=datetime(2025, 10, 5)),
            Transaction(credit=300_000, customer=cls.c2, date=datetime(2025, 10, 5)),
            Transaction(debit=20_000, customer=cls.c3, date=datetime(2025, 10, 5)),
            Transaction(credit=150_000, customer=cls.c1, date=datetime(2025, 10, 6)),
            Transaction(credit=100_000, customer=cls.c2, date=datetime(2025, 10, 6)),
            Transaction(credit=10_000, customer=cls.c3, date=datetime(2025, 10, 6)),
            Transaction(debit=50_000, customer=cls.c1, date=datetime(2025, 10, 7)),
            Transaction(debit=40_000, customer=cls.c2, date=datetime(2025, 10, 7)),
            Transaction(credit=10_000, customer=cls.c3, date=datetime(2025, 10, 7)),
        ]

        for trans in transactions:
            trans.save()

    @classmethod
    def tearDownClass(cls):
        Transaction.objects.all().delete()
        Customer.objects.all().delete()
