from rest_framework.routers import SimpleRouter

from stock import apis

app_name = "stock"

router = SimpleRouter()
router.register(r"product", apis.ProductViewSet, basename="products")
router.register(r"order", apis.OrderViewSet, basename="orders")

urlpatterns = router.urls
