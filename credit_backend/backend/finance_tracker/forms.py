from django import forms
from backend.finance_tracker.models import Transaction

class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)
    currency = forms.ChoiceField(choices=Transaction.CURRENCY_CHOICES)

    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'category', 'date', 'description', 'currency']
