import pytest
from django.conf import settings
from django.test import Client
from model_bakery import baker

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup_client(client):
    user = baker.make(settings.AUTH_USER_MODEL)
    fruit = baker.make("fruits.Fruit", name="みかん")
    baker.make("sales.Sale", fruit=fruit)
    client.force_login(user)


def test_top(client):
    response = client.get("/summary/", follow=True)

    assert response.status_code == 200
    assert "みかん" in response.content.decode("utf-8")


def test_top_with_no_login():
    client = Client()

    response = client.get("/summary/", follow=True)

    assert response.status_code == 200
