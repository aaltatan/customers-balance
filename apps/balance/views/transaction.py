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
        queryset = Transaction.objects.annotate_net().select_related("customer")

        if self.request.user.has_perm("balance.view_deleted_transactions"):
            return queryset

        return queryset.filter(is_deleted=False)
