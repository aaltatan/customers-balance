from django.urls import path

from apps.balance.views import transaction

app_name = "transaction"

urlpatterns = [
    path("", transaction.TransactionListView.as_view(), name="index"),
    path("<str:slug>/", transaction.LedgerListView.as_view(), name="ledger"),
    path(
        "create/debit/<str:customer_slug>/",
        transaction.DebitTransactionCreateView.as_view(),
        name="create-debit",
    ),
    path(
        "create/credit/<str:customer_slug>/",
        transaction.CreditTransactionCreateView.as_view(),
        name="create-credit",
    ),
]
