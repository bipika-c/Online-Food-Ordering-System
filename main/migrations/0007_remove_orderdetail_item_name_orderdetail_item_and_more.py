# Generated by Django 5.0.4 on 2024-06-14 17:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_user_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='item_name',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.food_items'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
