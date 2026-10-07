from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, CategoryViewSet, ProductViewSet, CartViewSet, OrderViewSet

router = DefaultRouter()
router.register("auth/register", RegisterViewSet, basename="register")
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("cart", CartViewSet, basename="cart")
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [path("", include(router.urls))]
