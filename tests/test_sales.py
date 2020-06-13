from datetime import datetime

import pytest
from django.conf import settings
from model_bakery import baker
from rest_framework.test import APIClient

from sales.models import Sale

pytestmark = pytest.mark.django_db


@pytest.fixture()
def api_client():
    user = baker.make(settings.AUTH_USER_MODEL)
    client = APIClient()
    client.force_login(user)
    return client


@pytest.fixture
def sale():
    fruit = baker.make("fruits.Fruit", id=999, name="みかん")
    sale = baker.make("sales.Sale", id=999, fruit=fruit)
    return sale


def test_top(api_client, sale):
    response = api_client.get("/api/sales/")

    assert response.status_code == 200
    assert response.json()[0]["id"] == sale.id


def test_top_with_no_login():
    api_client = APIClient()

    response = api_client.get("/api/sales/")

    assert response.status_code == 403


def test_new_submit(api_client, sale):
    response = api_client.post(
        "/api/sales/",
        data={
            "fruit": 999,
            "number": 1,
            "amount": 100,
            "sold_at": datetime(2018, 12, 13, 12, 13, 0),
        },
        format="json",
    )

    assert response.status_code == 201


def test_new_submit_with_wrong_data(api_client, sale):
    response = api_client.post(
        "/api/sales/",
        data={
            "fruit": 2,
            "number": 1,
            "amount": 100,
            "sold_at": datetime(2018, 12, 13, 12, 13, 0),
        },
        format="json",
    )

    assert response.status_code == 400


def test_edit_submit(api_client, sale):
    response = api_client.patch(
        "/api/sales/999/",
        data={
            "fruit": 999,
            "number": 1,
            "amount": 100,
            "sold_at": datetime(2018, 12, 14, 12, 14, 0),
        },
        format="json",
    )

    assert response.status_code == 200


def test_edit_submit_with_wrong_data(api_client, sale):
    response = api_client.patch(
        "/api/sales/999/",
        data={
            "fruit": 2,
            "number": 1,
            "amount": 100,
            "sold_at": datetime(2018, 12, 14, 12, 14, 0),
        },
        format="json",
    )

    assert response.status_code == 400


def test_delete_submit(api_client, sale):
    # arrange
    assert Sale.objects.count() == 1

    # act
    response = api_client.delete(f"/api/sales/{sale.id}/", format="json")

    # assert
    assert response.status_code == 204
    assert Sale.objects.count() == 0


def test_delete_with_wrong_data(api_client, sale):
    # act
    response = api_client.delete(f"/api/sales/0/", format="json")

    # assert
    assert response.status_code == 404
