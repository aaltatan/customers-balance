from typing import Any

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.balance.forms import CreditTransactionForm, DebitTransactionForm
from apps.balance.models import Customer, Transaction
from apps.core.views import CreateView, ListView


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


class DebitTransactionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "balance.add_transaction"
    form_class = DebitTransactionForm
    template_name = "apps/balance/transaction/create.html"
    partial_template_name = "cotton/balance/transaction/modal_create_debit.html"

    def get_initial(self) -> dict[str, Any]:
        customer_slug = self.request.resolver_match.kwargs["customer_slug"]
        customer = get_object_or_404(Customer, slug=customer_slug)
        return {"customer": customer}

    def get_create_url(self):
        customer_slug = self.request.resolver_match.kwargs["customer_slug"]
        return reverse(
            "balance:transaction:create-debit",
            kwargs={"customer_slug": customer_slug},
        )


class CreditTransactionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "balance.add_transaction"
    form_class = CreditTransactionForm
    template_name = "apps/balance/transaction/create.html"
    partial_template_name = (
        "cotton/balance/transaction/modal_create_credit.html"
    )

    def get_initial(self) -> dict[str, Any]:
        customer_slug = self.request.resolver_match.kwargs["customer_slug"]
        customer = get_object_or_404(Customer, slug=customer_slug)
        return {"customer": customer, "credit": customer.get_net()}

    def get_create_url(self):
        customer_slug = self.request.resolver_match.kwargs["customer_slug"]
        return reverse(
            "balance:transaction:create-credit",
            kwargs={"customer_slug": customer_slug},
        )


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
