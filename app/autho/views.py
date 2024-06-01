from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from helpers.api_mixins import BaseAPIMixin
from helpers.documentation import api_document

from .filters import UserFilter
from .models import User
from .serializers import ReadOnlyUserSerializer, UserAuthTokenSerializer, UserSerializer


@api_document(names=["post"], tags=["Authentication"])
class ObtainAuthTokenView(BaseAPIMixin, APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        serializer = UserAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        user_serializer = UserSerializer(user)

        user_data = user_serializer.data
        user_data["token"] = token.key
        return self.api_success_response(user_data, message="Successfully logged in")


@api_document(names=["get"], tags=["User"])
class UserProfileAPI(BaseAPIMixin, APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return self.api_success_response(serializer.data)


@api_document(names=["list", "retrieve"], tags=["Filtering"])
class UserListViewset(BaseAPIMixin, ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = ReadOnlyUserSerializer
    pagination_class = None
    filter_class = UserFilter
    search_fields = ("name", "username", "email")

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset
        return queryset.filter(id=user.id)
