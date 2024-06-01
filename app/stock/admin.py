from django.contrib import admin
from .models import Product, Order


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "dry_weight", "wet_weight", "created_on")
    search_fields = ("product_name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "order_date", "production_date", "packing_date", "number_of_units")
    search_fields = ("customer", "product")
