from django.urls import path

from rest_framework.routers import SimpleRouter

from autho import views, apis

app_name = "autho"

router = SimpleRouter()
router.register(r"users", views.UserListViewset, basename="users")
router.register(r"customer", apis.CustomerViewset, basename="customer")
urlpatterns = router.urls

urlpatterns += [
    path("user/profile/", views.UserProfileAPI.as_view(), name="user-profile"),
]
