from django.urls import path
from ..views import transaction

app_name = "transaction"

urlpatterns = [
    path("", transaction.TransactionListView.as_view(), name="index"),
]
