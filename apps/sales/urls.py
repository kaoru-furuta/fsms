from django.conf.urls import include, url
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    r"", views.SaleViewSet, basename="sales",
)

urlpatterns = [
    url(r"", include(router.urls)),
]
