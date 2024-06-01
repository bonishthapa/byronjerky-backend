from django.contrib.auth import authenticate

from rest_framework import serializers

from helpers.serializer_mixins import BaseModelSerializer

from .models import User


class UserSerializer(BaseModelSerializer):
    roles = serializers.SerializerMethodField()
    ui_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "idx",
            "name",
            "username",
            "email",
            "roles",
            "ui_permissions",
        )

    def get_ui_permissions(self, obj):
        return obj.get_ui_permissions()

    def get_roles(self, obj):
        return obj.get_roles()


class ReadOnlyUserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = (
            "idx",
            "name",
            "username",
            "email",
        )


class UserAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", write_only=True, required=True)
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )
    token = serializers.CharField(label="Token", read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs