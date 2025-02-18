from django.db import models
from inventory.models import Inventory
from customers.models import Customer
from django.utils import timezone

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    date_sold = models.DateTimeField(auto_now_add=True)
    last_payment_update = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.balance = self.grand_total - self.paid
        super().save(*args, **kwargs)

        if self.paid > 0:
            Receipt.objects.create(
                sale=self, date_issued=self.date_sold, paid=self.paid, balance=self.balance
            )

    def update_payment(self, amount):
        self.paid += amount
        self.balance = self.grand_total - self.paid
        self.last_payment_update = timezone.now()
        self.save()

        Receipt.objects.create(
            sale=self, date_issued=self.last_payment_update, paid=self.paid, balance=self.balance
        )

    def __str__(self):
        return f"Sale {self.id} - {self.date_sold}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='saleitem')  # Ensure this is set
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.selling_price:  # Prevent overwriting on update
            self.selling_price = self.item.selling_price
        self.total = self.selling_price * self.quantity
        self.item.quantity -= self.quantity  # ✅ Reduce stock
        self.item.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.item.quantity += self.quantity  # ✅ Restore stock on delete
        self.item.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


class Receipt(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    date_issued = models.DateTimeField(default=timezone.now)  # Automatically set to current time
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Receipt {self.sale.id} - {self.date_issued}"
