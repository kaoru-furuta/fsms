from django.urls import path

from . import views

app_name = "sales"
urlpatterns = [
    path("", views.IndexView.as_view(), name="top"),
    path("new/", views.NewView.as_view(), name="new"),
    path("upload/", views.upload, name="upload"),
    path("<int:pk>/edit/", views.EditView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]
