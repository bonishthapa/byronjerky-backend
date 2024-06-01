from rest_framework import serializers

from core.models import FileUpload
from helpers.serializer_mixins import BaseModelSerializer
from helpers.storage import BaseMediaStorage


class FileUploadSerializer(BaseModelSerializer):
    class Meta:
        model = FileUpload
        fields = ("idx", "file")

    def create(self, validated_data):
        is_private = validated_data.get("is_private_to_user", False)
        if is_private:
            FileUpload.file.field.storage = BaseMediaStorage(scope="private_file")
        else:
            FileUpload.file.field.storage = BaseMediaStorage(scope="public_file")
        return super().create(validated_data)


class FileUploadReadSerializer(BaseModelSerializer):
    accessible_file_path = serializers.SerializerMethodField()

    class Meta:
        model = FileUpload
        fields = ("idx", "accessible_file_path")

    def get_accessible_file_path(self, instance):
        return instance.accessible_file_path if instance.file else ""
