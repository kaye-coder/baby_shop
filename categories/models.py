from django.db import models

class SemiCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    semi_category = models.ForeignKey(
        SemiCategory,
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.semi_category.name if self.semi_category else 'No SemiCategory'})"
