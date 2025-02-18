from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_create.html', {'form': form})

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_create.html', {'form': form})


def employee_delete(request, pk):
    if request.method == 'POST':  # Make sure it's POST, not DELETE
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return redirect('employee_list')  # Redirect back to the employee list
    return redirect('employee_list')  # If not POST, redirect to list
