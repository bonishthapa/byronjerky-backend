from rest_framework.viewsets import ModelViewSet

from helpers.api_mixins import BaseCRUDMixin
from .models import Role
from .serializers import ReadOnlyRoleSerializer


class RoleViewset(BaseCRUDMixin, ModelViewSet):
    queryset = Role.objects.filter(is_deleted=False)
    serializer_class = ReadOnlyRoleSerializer
    search_fields = ("name",)
