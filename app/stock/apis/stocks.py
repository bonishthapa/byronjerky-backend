from rest_framework.viewsets import ModelViewSet

from helpers.api_mixins import BaseCRUDMixin
from stock.models import Product, Order
from stock.serializers import (
    ProductListSerializer,
    OrderListSerializer,
    ProductSearchSerializer,
    OrderCreateSerializer,
    OrderDetailSerializer,
)
from stock.filters import OrderFilter


class ProductViewSet(BaseCRUDMixin, ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False).order_by('-created_date')
    serializer_class = ProductListSerializer
    search_fields = ['product_name']

    def get_serializer_class(self):
        if self.action == 'all':
            return ProductSearchSerializer
        return ProductListSerializer


class OrderViewSet(BaseCRUDMixin, ModelViewSet):
    queryset = Order.objects.filter(is_deleted=False).order_by('-created_date')
    serializer_class = OrderListSerializer
    search_fields = ['product__product_name', 'customer__first_name', 'customer__last_name']
    filterset_class = OrderFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.api_success_response(data="Order created successfully")
