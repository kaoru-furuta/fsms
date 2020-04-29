import pytest
from django.conf import settings
from model_bakery import baker

pytestmark = pytest.mark.django_db


def test_top(client):
    # arrange
    user = baker.make(settings.AUTH_USER_MODEL)
    client.force_login(user)

    # act
    response = client.get("/", follow=True)

    # assert
    assert response.status_code == 200
    assert "core/top.html" in response.template_name


def test_top_with_no_login(client):
    # act
    response = client.get("/", follow=True)

    # assert
    assert response.status_code == 200
    assert "registration/login.html" in response.template_name


def test_login(client):
    # arrange
    user = baker.make(settings.AUTH_USER_MODEL)
    user.set_password("password")
    user.save()

    # act
    response = client.post(
        "/login/",
        data={"username": user.username, "password": "password"},
        follow=True,
    )

    # assert
    assert response.status_code == 200
    assert "core/top.html" in response.template_name


def test_login_with_wrong_data(client):
    # arrange
    user = baker.make(settings.AUTH_USER_MODEL)
    user.set_password("password")
    user.save()

    # act
    response = client.post(
        "/login/",
        data={"username": user.username, "password": "wrong_password"},
        follow=True,
    )

    # assert
    assert response.status_code == 200
    assert "registration/login.html" in response.template_name
