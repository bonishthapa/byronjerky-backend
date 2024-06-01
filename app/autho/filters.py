from autho.models import User
from helpers.filter_mixins import BaseFilterSet


class UserFilter(BaseFilterSet):
    class Meta:
        model = User
        fields = [
            "idx",
            "name",
            "username",
            "email",
        ]
