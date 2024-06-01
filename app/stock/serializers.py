from datetime import timedelta

from rest_framework import serializers

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
    product = serializers.CharField(source='product.product_name')
    customer = serializers.CharField(source='customer.get_full_name')

    class Meta:
        model = Order
        fields = [
            'idx',
            'product',
            'order_date',
            'production_date',
            'packing_date',
            'number_of_units',
            'wet_weight',
            'customer',
        ]


class OrderCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Order
        fields = [
            'product',
            'order_date',
            'production_date',
            'packing_date',
            'number_of_units',
            'wet_weight',
            'customer',
        ]

    def create(self, validated_data):
        try:
            production_date = validated_data.pop('production_date', None)
            order_date = validated_data.pop('order_date', None)
            customer = validated_data.get('customer')
            if not production_date:
                lead_time_delta = timedelta(days=(customer.lead_time - 6))
                production_date = order_date + lead_time_delta

            packing_date = validated_data.pop('packing_date', None)
            if not packing_date:
                order_date_delta = timedelta(days=2)  # Assuming you want to subtract 2 days
                packing_date = production_date + order_date_delta

            wet_weight = validated_data.pop('wet_weight', None)
            number_of_units = validated_data.get('number_of_units', None)
            product = validated_data.get('product')
            if not wet_weight:
                wet_weight = product.wet_weight * number_of_units
        except Exception as e:
            raise serializers.ValidationError(str(e))

        order = Order.new(
            packing_date=packing_date,
            production_date=production_date,
            wet_weight=wet_weight,
            order_date=order_date,
            **validated_data
            )
        return order


class OrderDetailSerializer(BaseModelSerializer):
    product = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'idx',
            'product',
            'order_date',
            'production_date',
            'packing_date',
            'number_of_units',
            'wet_weight',
            'customer',
        ]

    def get_product(self, obj):
        return {
            'idx': obj.product.idx,
            'name': obj.product.product_name
        }

    def get_customer(self, obj):
        return {
            'idx': obj.customer.idx,
            'name': obj.customer.get_full_name
        }


class ProductSearchSerializer(BaseModelSerializer):
    name = serializers.CharField(source='product_name')

    class Meta:
        model = Product
        fields = ['idx', 'name']
