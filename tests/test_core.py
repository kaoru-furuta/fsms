import pytest
from django.conf import settings
from model_bakery import baker
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_login():
    # arrange
    user = baker.make(settings.AUTH_USER_MODEL)
    user.set_password("password")
    user.save()
    api_client = APIClient()

    # act
    response = api_client.post(
        "/api/login/",
        data={"username": user.username, "password": "password"},
        follow=True,
    )

    # assert
    assert response.status_code == 200


def test_login_with_wrong_data():
    # arrange
    user = baker.make(settings.AUTH_USER_MODEL)
    user.set_password("password")
    user.save()
    api_client = APIClient()

    # act
    response = api_client.post(
        "/api/login/",
        data={"username": user.username, "password": "wrong_password"},
        follow=True,
    )

    # assert
    assert response.status_code == 401
