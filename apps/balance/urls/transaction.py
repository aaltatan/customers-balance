from django.urls import path

from apps.balance.views import transaction

app_name = "transaction"

urlpatterns = [
    path("", transaction.TransactionListView.as_view(), name="index"),
    path("<str:slug>/", transaction.LedgerListView.as_view(), name="ledger"),
]
