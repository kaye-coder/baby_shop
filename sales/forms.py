from django import forms
from .models import Sale, SaleItem

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'paid']

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['item', 'quantity']
