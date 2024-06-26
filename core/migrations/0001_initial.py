# Generated by Django 4.2.5 on 2023-09-30 08:04

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import helpers.model_fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FileUpload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "idx",
                    helpers.model_fields.IDXField(
                        blank=True, editable=False, length=8, max_length=15, unique=True
                    ),
                ),
                (
                    "created_date",
                    helpers.model_fields.CreatedDateField(
                        db_index=True, editable=False
                    ),
                ),
                (
                    "deleted_on",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("file", models.FileField(upload_to=core.models.file_upload_path)),
                (
                    "file_type",
                    models.CharField(
                        choices=[("file", "Others"), ("image", "Image")],
                        default="file",
                        max_length=10,
                    ),
                ),
                ("is_private_to_user", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="file_uploads",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Config",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "idx",
                    helpers.model_fields.IDXField(
                        blank=True, editable=False, length=8, max_length=15, unique=True
                    ),
                ),
                (
                    "created_date",
                    helpers.model_fields.CreatedDateField(
                        db_index=True, editable=False
                    ),
                ),
                (
                    "deleted_on",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("app", models.CharField(max_length=20)),
                ("key", models.CharField(max_length=255)),
                ("value", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("feature_flag", models.BooleanField(default=True)),
            ],
            options={
                "unique_together": {("app", "key")},
            },
        ),
        migrations.CreateModel(
            name="ActionLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "idx",
                    helpers.model_fields.IDXField(
                        blank=True, editable=False, length=8, max_length=15, unique=True
                    ),
                ),
                (
                    "created_date",
                    helpers.model_fields.CreatedDateField(
                        db_index=True, editable=False
                    ),
                ),
                (
                    "deleted_on",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("meta", models.JSONField(blank=True, default=dict)),
                ("created_on", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("action", models.CharField(db_index=True, max_length=200)),
                ("action_obj_type", models.CharField(db_index=True, max_length=100)),
                ("action_obj_id", models.BigIntegerField(db_index=True)),
                ("remarks", models.TextField(null=True)),
                ("previous_state", models.JSONField(blank=True, default=dict)),
                ("next_state", models.JSONField(blank=True, default=dict)),
                (
                    "request_path",
                    models.CharField(db_index=True, max_length=300, null=True),
                ),
                ("query_string", models.TextField(null=True)),
                (
                    "request_method",
                    models.CharField(db_index=True, max_length=10, null=True),
                ),
                ("request_body", models.TextField(null=True)),
                ("request_meta", models.JSONField(blank=True, default=dict)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="actionlogs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
