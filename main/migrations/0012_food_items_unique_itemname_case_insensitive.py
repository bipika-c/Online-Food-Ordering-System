# Generated by Django 5.0.4 on 2024-06-16 11:46

import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_food_items_itemname'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='food_items',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('itemname'), name='unique_itemname_case_insensitive'),
        ),
    ]