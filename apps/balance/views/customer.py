from typing import Any

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from apps.core.views import ListView

from ..filters import CustomerFilterset
from ..models import Customer


class CustomerDetailView(PermissionRequiredMixin, View):
    permission_required = "balance.view_customer"
    model = Customer
    template_name = "cotton/balance/customer/detail.html"

    def get_template_name(self) -> str:
        return self.template_name

    def get(
        self,
        request: HttpRequest,
        *args: tuple[Any],
        slug: str,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        customer = get_object_or_404(self.model, slug=slug)
        template_name = self.get_template_name()
        context = {
            "object": customer,
        }
        response = render(request, template_name, context)
        response["HX-Trigger"] = "showmodal"
        return response


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
        return Customer.objects.annotate_totals().order_by("-net")
