from rest_framework.viewsets import ModelViewSet

from helpers.api_mixins import BaseAPIMixin
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewset(BaseAPIMixin, ModelViewSet):
    queryset = Customer.objects.filter(is_deleted=False)
    serializer_class = CustomerSerializer
    search_fields = ("user__email", "mobile", "first_name", "last_name")
