from django.urls import path

from . import views

app_name = 'summaries'
urlpatterns = [
    path('', views.IndexView.as_view(), name='top'),
]