from datetime import datetime

import pytest
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management import call_command
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.test import APIClient

from fruits.models import Fruit

pytestmark = pytest.mark.django_db


@pytest.fixture()
def api_client():
    user = baker.make(settings.AUTH_USER_MODEL)
    client = APIClient()
    client.force_login(user)
    return client


@pytest.fixture
def fruit_list():
    fruit_list = baker.make("fruits.Fruit", _quantity=10)
    fruit_list.sort(key=lambda x: x.updated_at)
    return fruit_list


def test_top(api_client, fruit_list):
    # act
    response = api_client.get("/api/fruits/")

    # assert
    assert response.status_code == 200
    assert response.json()[0]["id"] == fruit_list[0].id
    assert response.json()[-1]["id"] == fruit_list[-1].id


def test_top_with_no_login():
    # arrange
    api_client = APIClient()

    # act
    response = api_client.get("/api/fruits/")

    # assert
    assert response.status_code == 403


def test_new_submit(api_client):
    # arrange
    name = "りんご"
    price = 200
    filename = "りんご.png"
    image = ContentFile(b"image", name=filename)

    # act
    with freeze_time(datetime(2020, 5, 1, 0, 0, 0)):
        response = api_client.post(
            "/api/fruits/",
            data={"name": name, "price": price, "image": image},
            format="multipart",
        )

    # assert
    fruit = Fruit.objects.first()
    assert response.status_code == 201, response.json()
    assert fruit.name == name
    assert fruit.price == price
    assert fruit.image.name == filename


def test_new_submit_with_wrong_data(api_client):
    # act
    response = api_client.post(
        "/api/fruits/", data={"name": "みかん", "price": "foo"}, format="json"
    )

    # assert
    assert response.status_code == 400
    assert not Fruit.objects.filter(name="みかん").exists()


def test_edit_submit(api_client, fruit_list):
    # act
    response = api_client.patch(
        f"/api/fruits/{fruit_list[0].id}/",
        data={"name": "りんご", "price": 200},
        format="json",
    )

    # assert
    assert response.status_code == 200
    assert Fruit.objects.filter(name="りんご", price=200).exists()


def test_edit_submit_with_wrong_data(api_client, fruit_list):
    # act
    response = api_client.patch(
        f"/api/fruits/{fruit_list[0].id}/",
        data={"name": "りんご", "price": "foo"},
        format="json",
    )

    # assert
    assert response.status_code == 400
    assert not Fruit.objects.filter(name="りんご").exists()


def test_delete_submit(api_client):
    # arrange
    fruit = baker.make("fruits.Fruit")
    assert Fruit.objects.count() == 1

    # act
    response = api_client.delete(f"/api/fruits/{fruit.id}/", format="json")

    # assert
    assert response.status_code == 204
    assert Fruit.objects.count() == 0


def test_delete_with_wrong_data(api_client, fruit_list):
    # arrange
    assert Fruit.objects.count() == 10

    # act
    response = api_client.delete(f"/api/fruits/0/", format="json")

    # assert
    assert response.status_code == 404
    assert Fruit.objects.count() == 10


def test_command_update_prices():
    # arrange
    fruit = baker.make("fruits.Fruit", price=100)

    # act
    call_command("update_price")

    # assert
    fruit.refresh_from_db()
    assert fruit.price == 200
