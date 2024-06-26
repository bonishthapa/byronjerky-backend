# Generated by Django 4.2.5 on 2024-06-01 16:08

from django.db import migrations, models
import django.utils.timezone
import helpers.model_fields


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="created_date",
            field=helpers.model_fields.CreatedDateField(
                db_index=True, default=django.utils.timezone.now, editable=False
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="deleted_on",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="idx",
            field=helpers.model_fields.IDXField(
                blank=True, editable=False, length=8, max_length=15, unique=True
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="order",
            name="meta",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="order",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
