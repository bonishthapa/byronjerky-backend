from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = ("email", "username", "is_staff", "is_active", "is_superuser")
    list_filter = (
        "is_staff",
        "is_active",
    )
    readonly_fields = ("idx",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "idx",
                    "email",
                    "password",
                    "name",
                    "username",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "roles",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    filter_horizontal = ("roles",)
    search_fields = ("email",)
    ordering = ("email",)
