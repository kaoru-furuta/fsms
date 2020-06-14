from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    "", views.FruitViewSet, basename="fruits",
)

urlpatterns = [
    path("", include(router.urls)),
    path("download/<int:pk>/", views.download),
]
