from django import forms
from .models import Purchase

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['item', 'quantity', 'price', 'expiry_date', 'supplier']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

PurchaseFormSet = forms.modelformset_factory(Purchase, form=PurchaseForm, extra=1, can_delete=True)
