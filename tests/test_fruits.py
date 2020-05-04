import pytest
from django.conf import settings
from django.core.management import call_command
from django.test import Client
from model_bakery import baker

from fruits.models import Fruit

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup_client(client):
    user = baker.make(settings.AUTH_USER_MODEL)
    client.force_login(user)


@pytest.fixture
def fruit_list():
    fruit_list = baker.make("fruits.Fruit", _quantity=10)
    fruit_list.sort(key=lambda x: x.updated_at, reverse=True)
    return fruit_list


def test_top(client, fruit_list):
    # act
    response = client.get("/fruit/", follow=True)

    # assert
    assert response.status_code == 200
    assert "fruits/top.html" in response.template_name
    assert list(response.context["fruit_list"]) == fruit_list


def test_top_with_no_login():
    # arrange
    client = Client()

    # act
    response = client.get("/fruit/", follow=True)

    # assert
    assert response.status_code == 200
    assert "fruits/top.html" not in response.template_name


def test_new(client):
    # act
    response = client.get("/fruit/new/", follow=True)

    # assert
    assert response.status_code == 200
    assert "fruits/form.html" in response.template_name


def test_new_submit(client):
    # act
    response = client.post(
        "/fruit/new/", data={"name": "りんご", "price": 200}, follow=True
    )

    # assert
    assert response.status_code == 200
    assert "fruits/top.html" in response.template_name
    assert Fruit.objects.filter(name="りんご", price=200).exists()


def test_new_submit_with_wrong_data(client):
    # act
    response = client.post(
        "/fruit/new/", data={"name": "みかん", "price": "foo"}, follow=True
    )

    # assert
    assert response.status_code == 200
    assert "fruits/form.html" in response.template_name
    assert not Fruit.objects.filter(name="みかん").exists()


def test_edit(client, fruit_list):
    # act
    response = client.get("/fruit/1/edit/", follow=True)

    # assert
    assert response.status_code == 200
    assert "fruits/form.html" in response.template_name


def test_edit_submit(client, fruit_list):
    # act
    response = client.post(
        "/fruit/1/edit/", data={"name": "りんご", "price": 200}, follow=True
    )

    # assert
    assert response.status_code == 200
    assert "fruits/top.html" in response.template_name
    assert Fruit.objects.filter(name="りんご", price=200).exists()


def test_edit_submit_with_wrong_data(client, fruit_list):
    # act
    response = client.post(
        "/fruit/1/edit/", data={"name": "りんご", "price": "foo"}, follow=True
    )

    # assert
    assert response.status_code == 200
    assert "fruits/form.html" in response.template_name
    assert not Fruit.objects.filter(name="りんご").exists()


def test_delete_submit(client):
    # arrange
    fruit = baker.make("fruits.Fruit")
    assert Fruit.objects.count() == 1

    # act
    response = client.post(
        f"/fruit/delete/", data={f"option-{fruit.id}": "delete"}, follow=True
    )

    # assert
    assert response.status_code == 200
    assert "fruits/top.html" in response.template_name
    assert Fruit.objects.count() == 0


def test_delete_with_wrong_data(client, fruit_list):
    # arrange
    assert Fruit.objects.count() == 10

    # act
    response = client.post(f"/fruit/delete/", data={f"option-0": "delete"}, follow=True)

    # assert
    assert response.status_code == 200
    assert "fruits/top.html" in response.template_name
    assert Fruit.objects.count() == 10


def test_command_update_prices():
    # arrange
    fruit = baker.make("fruits.Fruit", price=100)

    # act
    call_command("update_price")

    # assert
    fruit.refresh_from_db()
    assert fruit.price == 200
