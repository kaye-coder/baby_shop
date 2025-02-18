# Generated by Django 5.1.6 on 2025-02-14 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sale',
            name='grand_total',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=10),
        ),
    ]
