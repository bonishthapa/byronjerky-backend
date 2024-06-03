from rest_framework.routers import SimpleRouter

from permission import apis

app_name = "permission"

router = SimpleRouter()
router.register(r"roles", apis.RoleViewset, basename="roles")
urlpatterns = router.urls
