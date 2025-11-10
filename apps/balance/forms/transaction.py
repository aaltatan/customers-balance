from django import forms

from apps.balance.models import Transaction


class DebitTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("debit", "customer", "notes")


class CreditTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("credit", "customer", "notes")
