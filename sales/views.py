from django.shortcuts import render, get_object_or_404, redirect
from .models import Sale, SaleItem, Receipt
from inventory.models import Inventory
from customers.models import Customer
from .forms import SaleForm, SaleItemForm
from django.utils.timezone import now
from decimal import Decimal
from django.db import transaction

def sales_list(request):
    # Order sales by 'date_sold' in descending order (newest first)
    sales = Sale.objects.all().prefetch_related('saleitem__item').order_by('-date_sold')
    return render(request, 'sales/sales_list.html', {'sales': sales})

def sales_create(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer")
        items = request.POST.getlist("item")
        quantities = request.POST.getlist("quantity")
        paid_amount = Decimal(request.POST.get("paid"))

        total_amount = Decimal(0)

        with transaction.atomic():
            # Create Sale record
            sale = Sale.objects.create(
                customer_id=customer_id,
                grand_total=0,  # Will be updated later
                paid=paid_amount,
                balance=0,  # Will be updated later
            )

            # Create SaleItems and calculate total
            for i in range(len(items)):
                item = Inventory.objects.get(id=items[i])
                quantity = int(quantities[i])
                selling_price = item.selling_price
                total = selling_price * quantity

                SaleItem.objects.create(
                    sale=sale,
                    item=item,
                    quantity=quantity,
                    selling_price=selling_price,
                    total=total,
                )

                total_amount += total

            # Update Sale with grand total and balance
            sale.grand_total = total_amount
            sale.balance = total_amount - paid_amount
            sale.save()

        # Redirect to the receipt page with sale details
        return redirect('sales_receipt', sale_id=sale.id)

    # Handle GET request, return the sale creation page
    customers = Customer.objects.all()
    inventory = Inventory.objects.all()
    return render(request, "sales_create.html", {"customers": customers, "inventory": inventory})

def sales_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    sale_items = sale.saleitem.all()  # Use the correct related name here
    receipts = sale.receipt_set.all()

    return render(request, 'sales/sales_receipt.html', {
        'sale': sale,
        'sale_items': sale_items,
        'receipts': receipts
    })


def update_payment(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == "POST":
        amount = Decimal(request.POST.get('amount'))  # Convert to Decimal
        if amount <= 0:
            return render(request, 'sales/update_payment.html', {'sale': sale, 'error': "Invalid amount!"})

        # Update payment and create a receipt
        balance = sale.grand_total - (sale.paid + amount)  # New balance
        receipt = Receipt.objects.create(
            sale=sale,
            paid=amount,
            balance=balance
        )

        # Update the Sale's paid amount and balance
        sale.paid += amount
        sale.balance = sale.grand_total - sale.paid
        sale.save()

        # After updating payment, redirect to the receipt page
        return redirect('sales_receipt', sale_id=sale.id)

    return render(request, 'sales/update_payment.html', {'sale': sale})

def sales_delete(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        sale.delete()  # Delete the sale
        return redirect('sales_list')  # Redirect to the sales list page
    return redirect('sales_list')

