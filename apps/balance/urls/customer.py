from django.urls import path
from ..views import customer

app_name = "customer"

urlpatterns = [
    path("", customer.CustomerListView.as_view(), name="index"),
]
