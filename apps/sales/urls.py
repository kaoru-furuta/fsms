from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    "", views.SaleViewSet, basename="sales",
)

urlpatterns = [
    path("", include(router.urls)),
]
