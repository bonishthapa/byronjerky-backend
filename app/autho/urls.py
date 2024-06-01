from django.urls import path

from rest_framework.routers import SimpleRouter

from autho import views

app_name = "autho"

router = SimpleRouter()
router.register(r"users", views.UserListViewset, basename="users")
urlpatterns = router.urls

urlpatterns += [
    path("user/profile/", views.UserProfileAPI.as_view(), name="user-profile"),
]
