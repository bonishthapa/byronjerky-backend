from rest_framework.authentication import TokenAuthentication


class BaseTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        return super().authenticate(request)
