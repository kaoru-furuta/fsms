from django.urls import path

from . import views

app_name = "fruits"
urlpatterns = [
    path("", views.IndexView.as_view(), name="top"),
    path("new/", views.NewView.as_view(), name="new"),
    path("<int:pk>/edit/", views.EditView.as_view(), name="edit"),
    path("delete/", views.delete, name="delete"),
]
