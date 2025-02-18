from django.db import models
from inventory.models import Inventory
from suppliers.models import Supplier


class Purchase(models.Model):
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Update Inventory
        inventory_item, created = Inventory.objects.get_or_create(
            name=self.item.name,
            unit=self.item.unit,
            category=self.item.category,
            defaults={'quantity': 0, 'purchasing_price': self.price}
        )

        inventory_item.quantity += self.quantity
        inventory_item.purchasing_price = self.price  # Update price
        inventory_item.expiry_date = self.expiry_date  # Update expiry if provided
        inventory_item.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} - {self.quantity} units"
