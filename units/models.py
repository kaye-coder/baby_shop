from django.db import models

class Unit(models.Model):
    abbreviation = models.CharField(max_length=10)
    full_form = models.CharField(max_length=100)

    def __str__(self):
        return self.abbreviation
