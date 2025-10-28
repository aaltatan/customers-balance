from django.contrib.auth.mixins import PermissionRequiredMixin

from apps.core.views import ListView

from ..models import Transaction


class TransactionListView(PermissionRequiredMixin, ListView):
    permission_required = "balance.view_transaction"
    model = Transaction
    search_fields = ("customer__name",)
    add_ordering_filterset = False
    paginate_by = 20

    def get_initial_queryset(self):
        return Transaction.objects.select_related("customer").order_by("-date")
