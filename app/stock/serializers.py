from helpers.serializer_mixins import BaseModelSerializer
# from helpers.serializer_fields import DetailRelatedField
from .models import Product, Order


class ProductListSerializer(BaseModelSerializer):
    class Meta:
        model = Product
        fields = ['idx', 'product_name', 'dry_weight', 'wet_weight']


class ProductDetailSerializer(BaseModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderListSerializer(BaseModelSerializer):
    class Meta:
        model = Order
        fields = ['idx', 'product', 'order_date', 'production_date', 'packing_date', 'number_of_units', 'wet_weight']


class OrderDetailSerializer(BaseModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
