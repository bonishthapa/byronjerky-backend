from rest_framework import serializers

from helpers.serializer_fields import BaseRelatedField


class BaseModelSerializer(serializers.ModelSerializer):
    serializer_related_field = BaseRelatedField
    idx = serializers.CharField(read_only=True)

    class Meta:
        exclude = ("id", "modified_on", "is_deleted")
        extra_kwargs = {
            "created_on": {"read_only": True},
            "modified_on": {"read_only": True},
        }
