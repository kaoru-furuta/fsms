from django.conf.urls import include, url
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    r"", views.FruitViewSet, basename="fruits",
)

urlpatterns = [
    url(r"", include(router.urls)),
]
