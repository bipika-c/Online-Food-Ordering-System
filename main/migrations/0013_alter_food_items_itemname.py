# Generated by Django 5.0.4 on 2024-06-16 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_food_items_unique_itemname_case_insensitive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_items',
            name='itemname',
            field=models.CharField(max_length=200),
        ),
    ]