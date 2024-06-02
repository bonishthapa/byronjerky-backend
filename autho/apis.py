from rest_framework.viewsets import ModelViewSet

from helpers.api_mixins import BaseCRUDMixin
from .models import Customer
from .serializers import CustomerSerializer, CustomerCreateSerializer, CustomerSearchSerializer


class CustomerViewset(BaseCRUDMixin, ModelViewSet):
    queryset = Customer.objects.filter(is_deleted=False)
    serializer_class = CustomerSerializer
    search_fields = ("user__email", "mobile", "first_name", "last_name")

    def get_serializer_class(self):
        if self.action == "create":
            return CustomerCreateSerializer
        elif self.action == "all":
            return CustomerSearchSerializer
        return CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.api_success_response(data="Customer created successfully")
