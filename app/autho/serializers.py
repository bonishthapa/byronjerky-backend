from django.contrib.auth import authenticate
from django.db import IntegrityError

from rest_framework import serializers

from helpers.serializer_mixins import BaseModelSerializer
from .models import User, Customer


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


class CustomerSerializer(BaseModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "idx",
            "first_name",
            "last_name",
            "business_name",
            "mobile",
            "address",
            "city",
            "country",
            "zip_code",
            "lead_time",
            "name",
            "email"
        ]

    def get_name(self, obj):
        return obj.user.name

    def get_email(self, obj):
        return obj.user.email


class CustomerCreateSerializer(BaseModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=False)

    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "business_name",
            "mobile",
            "address",
            "city",
            "country",
            "zip_code",
            "lead_time",
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', "password")
        if not username:
            username = email
        user_data = {
            'email': email,
            'username': username,
            'password': password,
        }
        try:
            user = User.objects.create(**user_data)
        except IntegrityError:
            raise serializers.ValidationError({"email": 'User with this email already exists'})
        customer = Customer.new(user=user, **validated_data)
        return customer
