# Generated by Django 4.2.5 on 2024-06-02 14:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0002_order_created_date_order_created_on_order_deleted_on_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="is_archived",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Ordered", "Ordered"),
                    ("In Production", "In Production"),
                    ("Produced", "Produced"),
                    ("In Packing", "In Packing"),
                    ("Packed", "Packed"),
                    ("Delivered", "Delivered"),
                ],
                default="Ordered",
                max_length=20,
            ),
        ),
    ]
