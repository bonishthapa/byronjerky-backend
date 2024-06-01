from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

# from rest_framework import permissions
from autho.views import ObtainAuthTokenView

# from drf_yasg2.views import get_schema_view
# from drf_yasg2 import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Genesis API",
#         default_version="v1",
#         description="Genesis API",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="ajaykarki@gmail.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.IsAdminUser,),
# )


def index_view(request):
    return HttpResponse(
        "<pre style='padding:5em'>This page is kept blank intentionally</pre>"
    )


urlpatterns = []

versioned_urlpatterns = [
    path("api/v1/login/", ObtainAuthTokenView.as_view(), name="login"),
    path("api/v1/autho/", include("autho.urls")),
    path("api/v1/core/", include("core.urls")),
    path(
        "api/v1/autho/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]

unversioned_patterns = [
    # path(
    #     "genesis/swagger/",
    #     schema_view.with_ui("swagger", cache_timeout=0),
    #     name="schema-swagger-ui",
    # ),
    # path("genesis/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("byronjerky/", admin.site.urls),
    path("", index_view),
]

urlpatterns = unversioned_patterns + versioned_urlpatterns

if settings.DEBUG is True:
    import debug_toolbar

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
