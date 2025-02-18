from django.db import models
from categories.models import Category
from units.models import Unit

class Inventory(models.Model):
    name = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    expiry_date = models.DateField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    purchasing_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'unit', 'category')

    def save(self, *args, **kwargs):
        self.purchasing_price = float(self.purchasing_price)
        self.quantity = int(self.quantity)
        self.cost_per_item = self.purchasing_price
        self.total_cost = self.purchasing_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.unit.abbreviation}) - {self.category.name}"
