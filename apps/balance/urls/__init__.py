from django.urls import path, include


patterns = [
    path("", include("apps.balance.urls.customer"))
]