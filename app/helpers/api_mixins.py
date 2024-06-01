from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from permission.permission_mixins import GBasePermission

from .versioning import GBaseVersioning


class BaseAPIMixin:
    lookup_field = "idx"
    versioning_class = GBaseVersioning
    permission_classes = [GBasePermission]

    def api_error_response(
        self, data, response_code=status.HTTP_400_BAD_REQUEST, message="Error"
    ):
        return Response(
            {"data": data, "status": response_code, "message": message},
            status=response_code,
        )

    def api_success_response(
        self, data, response_code=status.HTTP_200_OK, message="Success"
    ):
        response_json = {"data": data, "status": response_code, "message": message}
        return Response(response_json, status=response_code)


class BaseListMixin(BaseAPIMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return self.api_success_response(serializer.data)

    @action(methods=["get"], detail=False)
    def all(self, request, *args, **kwargs):
        if hasattr(self, "filterset_class"):
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.get_queryset()
        if not request.query_params:
            queryset = queryset.none()
        serializer = self.get_serializer(queryset, many=True)
        return self.api_success_response(serializer.data)


class BaseReadOnlyMixin(BaseListMixin):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.api_success_response(serializer.data)


class BaseCRUDMixin(BaseListMixin):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.api_success_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.api_success_response(
            serializer.data,
            response_code=201,
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            data=request.data, instance=instance, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.api_success_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return self.api_success_response()
