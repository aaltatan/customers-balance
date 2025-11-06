from typing import Any

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.balance.models import Customer, Transaction
from apps.core.views import ListView


class TransactionListView(PermissionRequiredMixin, ListView):
    permission_required = "balance.view_transaction"
    model = Transaction
    search_fields = ("customer__name",)
    add_ordering_filterset = False

    def get_initial_queryset(self):
        queryset = Transaction.objects.annotate_net().select_related("customer")

        if self.request.user.has_perm("balance.view_deleted_transactions"):
            return queryset

        return queryset.filter(is_deleted=False)


class LedgerListView(PermissionRequiredMixin, ListView):
    permission_required = "balance.view_transaction"
    model = Transaction
    add_ordering_filterset = False
    add_search_filterset = False
    template_name = "apps/balance/ledger/list.html"
    partial_template_name = "cotton/balance/ledger/partial_list.html"

    def get_index_url(self):
        return reverse("balance:transaction:ledger", kwargs={"slug": self.slug})

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["customer"] = self.customer
        return context

    def get_initial_queryset(self):
        self.slug = self.request.resolver_match.kwargs["slug"]
        self.customer = get_object_or_404(Customer, slug=self.slug)
        queryset = (
            Transaction.objects.annotate_net()
            .select_related("customer")
            .filter(customer=self.customer)
        )

        if self.request.user.has_perm("balance.view_deleted_transactions"):
            return queryset

        return queryset.filter(is_deleted=False)
