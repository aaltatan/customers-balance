from django import forms

from apps.balance.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "mobile", "notes")
