import pytest
from django.conf import settings
from django.core.management import call_command
from django.test import Client
from model_bakery import baker

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup_client(client):
    user = baker.make(settings.AUTH_USER_MODEL)
    baker.make("fruits.Fruit", name="みかん")
    client.force_login(user)


def test_top(client):
    response = client.get("/fruit/", follow=True)

    assert response.status_code == 200
    assert "みかん" in response.content.decode("utf-8"), response.content.decode("utf-8")


def test_top_with_no_login():
    client = Client()

    response = client.get("/fruit/", follow=True)

    assert response.status_code == 200


def test_new(client):
    response = client.get("/fruit/new/", follow=True)

    assert response.status_code == 200


def test_new_with_no_login():
    client = Client()

    response = client.get("/fruit/new/", follow=True)

    assert response.status_code == 200


def test_new_submit(client):
    response = client.post(
        "/fruit/new/", data={"name": "りんご", "price": 200}, follow=True
    )

    assert response.status_code == 200
    assert "りんご" in response.content.decode("utf-8")


def test_new_submit_with_no_login():
    client = Client()

    response = client.post(
        "/fruit/new/", data={"name": "りんご", "price": 200}, follow=True
    )

    assert response.status_code == 200


def test_new_submit_with_wrong_data(client):
    response = client.post(
        "/fruit/new/", data={"name": "みかん", "price": "foo"}, follow=True
    )

    assert response.status_code == 200


def test_edit(client):
    response = client.get("/fruit/1/edit/", follow=True)

    assert response.status_code == 200


def test_edit_with_no_login():
    client = Client()

    response = client.get("/fruit/1/edit/", follow=True)

    assert response.status_code == 200


def test_edit_submit(client):
    response = client.post(
        "/fruit/1/edit/", data={"name": "りんご", "price": 200}, follow=True
    )

    assert response.status_code == 200
    assert "りんご" in response.content.decode("utf-8")


def test_edit_submit_with_no_login():
    client = Client()

    response = client.post(
        "/fruit/1/edit/", data={"name": "りんご", "price": 200}, follow=True
    )

    assert response.status_code == 200


def test_edit_submit_with_wrong_data(client):
    response = client.post(
        "/fruit/1/edit/", data={"name": "りんご", "price": "foo"}, follow=True
    )

    assert response.status_code == 200


def test_delete_submit(client):
    response = client.post("/fruit/1/delete/", follow=True)

    assert response.status_code == 200
    assert "みかん" not in response.content.decode("utf-8")


def test_delete_with_no_login():
    client = Client()

    response = client.post("/fruit/1/delete/", follow=True)

    assert response.status_code == 200


def test_delete_with_wrong_data(client):
    response = client.post("/fruit/2/delete/", follow=True)

    assert response.status_code == 200
    assert "みかん" in response.content.decode("utf-8")


def test_command_update_prices():
    # arrange
    fruit = baker.make("fruits.Fruit", price=100)

    # act
    call_command("update_price")

    # assert
    fruit.refresh_from_db()
    assert fruit.price == 200
