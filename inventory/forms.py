from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'unit', 'category', 'expiry_date', 'purchasing_price', 'selling_price', 'quantity']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'purchasing_price': forms.NumberInput(attrs={'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'min': '1'}),
        }
