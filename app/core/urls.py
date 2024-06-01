from rest_framework.routers import SimpleRouter

from core import views

router = SimpleRouter()
router.register(
    r"upload/file/public",
    views.PublicFileUploadAPIViewSet,
    basename="public-file-upload",
)
router.register(
    r"upload/file/private",
    views.PrivateFileUploadAPIViewSet,
    basename="private-file-upload",
)

urlpatterns = router.urls

urlpatterns += []
