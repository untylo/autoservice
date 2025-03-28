# Generated by Django 5.1.7 on 2025-03-19 07:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_part_service_supplier_inventory_repairorder_invoice_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='repairorder',
            name='workers',
            field=models.ManyToManyField(related_name='repair_orders', to=settings.AUTH_USER_MODEL, verbose_name='Работники'),
        ),
        migrations.CreateModel(
            name='RepairOrderPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='repair_photos/', verbose_name='Фото')),
                ('before_repair', models.BooleanField(default=True, verbose_name='До ремонта')),
                ('repair_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='cars.repairorder')),
            ],
        ),
    ]
