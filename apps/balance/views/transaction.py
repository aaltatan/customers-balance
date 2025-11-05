from django.contrib.auth.mixins import PermissionRequiredMixin

from apps.balance.models import Transaction
from apps.core.views import ListView


class TransactionListView(PermissionRequiredMixin, ListView):
    permission_required = "balance.view_transaction"
    model = Transaction
    search_fields = ("customer__name",)
    add_ordering_filterset = False
    paginate_by = 20

    def get_initial_queryset(self):
        return (
            Transaction.objects.annotate_net()
            .select_related("customer")
            .order_by("-date")
        )
