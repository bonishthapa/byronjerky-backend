from rest_framework import serializers

from .models import Role


class ReadOnlyRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("name", "idx")
