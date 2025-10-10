from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _

from apps.core.views import ListView

from ..filters import CustomerFilterset
from ..models import Customer


class CustomerListView(PermissionRequiredMixin, ListView):
    permission_required = "balance.view_customer"
    model = Customer
    filterset_class = CustomerFilterset
    search_fields = ("name", "mobile", "notes")
    ordering_fields = {
        "name": _("name"),
        "total_debit": _("total debit"),
        "total_credit": _("total credit"),
        "net": _("net"),
    }

    def get_initial_queryset(self):
        return Customer.objects.annotate_totals()
