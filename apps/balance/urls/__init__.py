from django.urls import include, path

patterns = [
    path("", include("apps.balance.urls.customer")),
    path("transactions/", include("apps.balance.urls.transaction")),
]
