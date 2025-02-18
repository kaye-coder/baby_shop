from django import forms
from .models import Category, SemiCategory

class SemiCategoryForm(forms.ModelForm):
    class Meta:
        model = SemiCategory
        fields = ["name"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "semi_category"]
