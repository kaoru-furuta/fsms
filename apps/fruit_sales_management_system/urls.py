from django.contrib import admin
from django.urls import include, path

from core.views import LoginView, LogoutView, MeView

urlpatterns = [
    path("api/fruits/", include("fruits.urls")),
    path("api/sales/", include("sales.urls")),
    path("api/login/", LoginView.as_view()),
    path("api/logout/", LogoutView.as_view()),
    path("api/me/", MeView.as_view()),
    path("admin/", admin.site.urls),
]
