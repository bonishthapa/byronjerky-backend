from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from helpers.api_mixins import BaseListMixin
from helpers.documentation import api_document

from .models import FileUpload
from .serializers import FileUploadReadSerializer, FileUploadSerializer


@api_document(names=["*"], tags=["Public Uploads"])
class PublicFileUploadAPIViewSet(BaseListMixin, ModelViewSet):
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.filter(is_private_to_user=False)

    def create(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.save(user=request.user)
        return self.api_success_response(
            {
                "media_url": file.file.url,
            },
            http_code=status.HTTP_201_CREATED,
        )

    # @TODO:
    def presigned(self, request, *args, **kwargs):
        raise NotImplementedError


@api_document(names=["*"], tags=["Private Uploads"])
class PrivateFileUploadAPIViewSet(BaseListMixin, ModelViewSet):
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.none()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FileUploadReadSerializer
        return self.serializer_class

    def get_queryset(self, *args, **kwargs):
        return FileUpload.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.save(is_private_to_user=True, user=request.user)
        return self.api_success_response(
            {
                "media_url": file.accessible_file_path,
            },
            http_code=status.HTTP_201_CREATED,
        )
