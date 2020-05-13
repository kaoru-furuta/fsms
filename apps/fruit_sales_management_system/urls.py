from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("fruit/", include("fruits.urls")),
    path("sale/", include("sales.urls")),
    path("summary/", include("summaries.urls")),
    path("login/", auth_views.LoginView.as_view()),
    path("admin/", admin.site.urls),
]

# FIXME: 開発時にアップロードデータを表示するために暫定的に設定
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
