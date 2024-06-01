from django.db import models
from datetime import timedelta

from helpers.models import BaseModel
# Create your models here.


class Product(BaseModel):
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    dry_weight = models.DecimalField(max_digits=10, decimal_places=2, help_text='Weight in grams')
    wet_weight = models.DecimalField(max_digits=10, decimal_places=2, help_text='Weight in grams')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Order(models.Model):
    customer = models.ForeignKey("autho.Customer", on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField()
    production_date = models.DateField(blank=True, null=True)
    packing_date = models.DateField(blank=True, null=True)
    number_of_units = models.IntegerField()
    wet_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.production_date:
            lead_time_delta = timedelta(days=(self.customer.lead_time - 6))
            self.production_date = self.order_date + lead_time_delta
        if not self.packing_date:
            order_date_delta = timedelta(days=2)  # Assuming you want to subtract 2 days
            self.packing_date = self.production_date + order_date_delta
        if not self.wet_weight:
            self.wet_weight = self.product.wet_weight * self.number_of_units
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'