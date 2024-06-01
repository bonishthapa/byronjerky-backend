from django.db import models

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


class Order(BaseModel):
    customer = models.ForeignKey("autho.Customer", on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField()
    production_date = models.DateField(blank=True, null=True)
    packing_date = models.DateField(blank=True, null=True)
    number_of_units = models.IntegerField()
    wet_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    @classmethod
    def new(cls, **kwargs):
        return cls.objects.create(**kwargs)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'