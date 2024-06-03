from helpers.filter_mixins import BaseFilterSet

from stock.models import Order


class OrderFilter(BaseFilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'is_archived': ['exact'],
        }