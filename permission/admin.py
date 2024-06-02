from django.contrib import admin

from .models import Permission, Role


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "method", "description")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    filter_horizontal = ("permissions",)
