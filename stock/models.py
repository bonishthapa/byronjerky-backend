from django.db import models

from helpers.models import BaseModel
from permission.models import UserRole
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

    def can_retrieve(self, user):
        return user.iss(UserRole.get_admin_roles())

    def can_partial_update(self, user):
        return user.iss(UserRole.get_admin_roles())

    def can_destroy(self, user):
        return user.iss(UserRole.get_admin_roles())


class Order(BaseModel):

    ORDERED = 'Ordered'
    IN_PRODUCTION = 'In Production'
    PRODUCED = 'Produced'
    IN_PACKING = 'In Packing'
    PACKED = 'Packed'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

    STATUS_CHOICES = [
        (ORDERED, ORDERED),
        (IN_PRODUCTION, IN_PRODUCTION),
        (PRODUCED, PRODUCED),
        (IN_PACKING, IN_PACKING),
        (PACKED, PACKED),
        (SHIPPED, SHIPPED),
        (DELIVERED, DELIVERED),
    ]

    customer = models.ForeignKey("autho.Customer", on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField()
    production_date = models.DateField(blank=True, null=True)
    packing_date = models.DateField(blank=True, null=True)
    number_of_units = models.IntegerField()
    wet_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)
    created_by = models.ForeignKey("autho.User", on_delete=models.CASCADE, related_name='orders')

    @classmethod
    def new(cls, **kwargs):
        return cls.objects.create(**kwargs)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def can_retrieve(self, user):
        return user.iss(UserRole.get_admin_roles())

    def can_partial_update(self, user):
        return user.iss(UserRole.get_admin_roles())

    def can_destroy(self, user):
        return user.iss(UserRole.get_admin_roles())
