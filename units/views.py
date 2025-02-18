from django.shortcuts import render, redirect
from .forms import UnitForm
from .models import Unit

def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'unit_list.html', {'units': units})

def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm()
    return render(request, 'unit_create.html', {'form': form})
