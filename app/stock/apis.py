from rest_framework.viewsets import ModelViewSet
from helpers.api_mixins import BaseCRUDMixin
from .models import Product, Order
from .serializers import ProductListSerializer, OrderListSerializer


class ProductViewSet(BaseCRUDMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    search_fields = ['product_name']


class OrderViewSet(BaseCRUDMixin, ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    search_fields = ['product__product_name']
