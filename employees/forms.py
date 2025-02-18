from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'age', 'email', 'phone', 'address', 'position', 'department', 'hire_date', 'salary']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }
