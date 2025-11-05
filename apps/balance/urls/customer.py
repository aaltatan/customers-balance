from django.urls import path

from apps.balance.views import customer

app_name = "customer"

urlpatterns = [
    path("", customer.CustomerListView.as_view(), name="index"),
    path(
        "detail/<str:slug>/",
        customer.CustomerDetailView.as_view(),
        name="detail",
    ),
]
