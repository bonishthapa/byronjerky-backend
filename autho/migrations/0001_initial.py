# Generated by Django 4.2.5 on 2023-09-26 17:27

from django.db import migrations, models
import helpers.model_fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("permission", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
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
                ("name", models.CharField(blank=True, max_length=200)),
                ("username", models.CharField(max_length=50, unique=True)),
                ("email", models.EmailField(max_length=254, null=True, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "roles",
                    models.ManyToManyField(
                        blank=True, related_name="users", to="permission.role"
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "ordering": ["-id"],
            },
        ),
    ]
