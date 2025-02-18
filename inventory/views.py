from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inventory, Unit, Category

def inventory_list(request):
    items = Inventory.objects.all().order_by('-created_at')
    total_cost = sum(item.purchasing_price * item.quantity for item in items)
    total_stock = sum(item.quantity for item in items)
    for item in items:
        item.total_cost = item.purchasing_price * item.quantity

    return render(request, 'inventory_list.html', {
        'items': items,
        'total_cost': total_cost,
        'total_stock': total_stock,
    })

def add_inventory(request):
    if request.method == 'POST':
        names = request.POST.getlist('name[]')
        units = request.POST.getlist('unit[]')
        categories = request.POST.getlist('category[]')
        expiry_dates = request.POST.getlist('expiry_date[]')
        purchasing_prices = request.POST.getlist('purchasing_price[]')
        selling_prices = request.POST.getlist('selling_price[]')
        quantities = request.POST.getlist('quantity[]')

        for i in range(len(names)):
            name = names[i]
            unit = get_object_or_404(Unit, id=units[i])
            category = get_object_or_404(Category, id=categories[i])
            expiry_date = expiry_dates[i]
            purchasing_price = purchasing_prices[i]
            selling_price = selling_prices[i]
            quantity = quantities[i]

            if Inventory.objects.filter(name=name, unit=unit, category=category).exists():
                messages.error(request, f"Item '{name}' already exists with the same unit and category.")
            else:
                Inventory.objects.create(
                    name=name,
                    unit=unit,
                    category=category,
                    expiry_date=expiry_date,
                    purchasing_price=purchasing_price,
                    selling_price=selling_price,
                    quantity=quantity
                )

        return redirect('inventory_list')

    units = Unit.objects.all()
    categories = Category.objects.all()
    return render(request, 'inventory_form.html', {'units': units, 'categories': categories})

def update_inventory(request, pk):
    item = get_object_or_404(Inventory, pk=pk)  # Get the item to update
    units = Unit.objects.all()  # Fetch all units
    categories = Category.objects.all()  # Fetch all categories

    if request.method == 'POST':
        # Extract the form data
        name = request.POST.get('name')
        unit_id = request.POST.get('unit')  # Get the unit ID from POST data
        category_id = request.POST.get('category')  # Get the category ID from POST data
        expiry_date = request.POST.get('expiry_date')
        purchasing_price = request.POST.get('purchasing_price')
        selling_price = request.POST.get('selling_price')
        quantity = request.POST.get('quantity')

        try:
            # Try to get the unit and category from the database
            unit = Unit.objects.get(id=unit_id)
            category = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            messages.error(request, "Unit or Category does not exist.")
            return redirect('inventory_list')  # Redirect back to the inventory list if not found

        # Update the item with the new values
        item.name = name
        item.unit = unit
        item.category = category
        item.expiry_date = expiry_date
        item.purchasing_price = purchasing_price
        item.selling_price = selling_price
        item.quantity = quantity

        item.save()  # Save the updated item

        messages.success(request, "Inventory updated successfully.")
        return redirect('inventory_list')  # Redirect to the inventory list after success

    return render(request, 'update_inventory.html', {
        'item': item,
        'units': units,
        'categories': categories
    })

def delete_inventory_item(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    item.delete()
    messages.success(request, "Item deleted successfully.")
    return redirect('inventory_list')
