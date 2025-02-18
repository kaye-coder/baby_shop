from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Purchase
from .forms import PurchaseFormSet
from inventory.models import Inventory
from suppliers.models import Supplier

@csrf_exempt
def create_purchase(request):
    items = Inventory.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        items_list = request.POST.getlist('item')
        quantities = request.POST.getlist('quantity')
        prices = request.POST.getlist('price')
        expiry_dates = request.POST.getlist('expiry_date')
        suppliers_list = request.POST.getlist('supplier')

        if items_list and quantities and prices and suppliers_list:
            for i in range(len(items_list)):
                try:
                    item = Inventory.objects.get(id=int(items_list[i]))
                    supplier = Supplier.objects.get(id=int(suppliers_list[i]))
                    quantity = int(quantities[i])
                    price = float(prices[i])
                    expiry_date = expiry_dates[i] if expiry_dates[i] else None

                    item.quantity += quantity
                    item.purchasing_price = price
                    item.save()

                    Purchase.objects.create(
                        item=item,
                        quantity=quantity,
                        price=price,
                        expiry_date=expiry_date,
                        supplier=supplier
                    )
                except (Inventory.DoesNotExist, Supplier.DoesNotExist, ValueError):
                    continue

            return redirect('purchase_list')

    return render(request, 'purchases/purchase_create.html', {
        'items': items,
        'suppliers': suppliers
    })

def purchase_list(request):
    purchases = Purchase.objects.all().order_by('-date_purchased')
    return render(request, 'purchases/purchase_list.html', {'purchases': purchases})

@csrf_exempt
def delete_purchase(request, pk):
    if request.method == 'POST':
        purchase = get_object_or_404(Purchase, pk=pk)
        inventory_item = purchase.item
        inventory_item.quantity -= purchase.quantity

        if inventory_item.quantity <= 0:
            inventory_item.delete()
        else:
            inventory_item.save()

        purchase.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
