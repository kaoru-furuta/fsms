import pytest
from django.conf import settings
from django.test import Client
from model_bakery import baker

from sales.models import Sale

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup_client(client):
    user = baker.make(settings.AUTH_USER_MODEL)
    fruit = baker.make("fruits.Fruit", name="みかん")
    baker.make("sales.Sale", id=1, fruit=fruit)
    client.force_login(user)


def test_top(client):
    response = client.get("/sale/", follow=True)

    assert response.status_code == 200
    assert "みかん" in response.content.decode("utf-8")


def test_top_with_no_login():
    client = Client()

    response = client.get("/sale/", follow=True)

    assert response.status_code == 200


def test_new(client):
    response = client.get("/sale/new/", follow=True)

    assert response.status_code == 200


def test_new_submit(client):
    response = client.post(
        "/sale/new/",
        data={"fruit_list": 1, "number": 1, "sold_at": "2018-12-13T12:13"},
        follow=True,
    )

    assert response.status_code == 200
    assert "2018/12/13 12:13" in response.content.decode("utf-8")


def test_new_submit_with_wrong_data(client):
    response = client.post(
        "/sale/new/",
        data={"fruit_list": 2, "number": 1, "sold_at": "2018-12-13T12:13"},
        follow=True,
    )

    assert response.status_code == 200


def test_edit(client):
    response = client.get("/sale/1/edit/", follow=True)

    assert response.status_code == 200


def test_edit_submit(client):
    response = client.post(
        "/sale/1/edit/",
        data={"fruit_list": 1, "number": 1, "sold_at": "2018-12-14T12:14"},
        follow=True,
    )

    assert response.status_code == 200
    assert "2018/12/14 12:14" in response.content.decode("utf-8")


def test_edit_submit_with_wrong_data(client):
    response = client.post(
        "/sale/1/edit/",
        data={"fruit_list": 2, "number": 1, "sold_at": "2018-12-14T12:14"},
        follow=True,
    )

    assert response.status_code == 200


def test_delete_submit(client):
    # arrange
    sale = baker.make("sales.Sale")
    assert Sale.objects.count() == 2

    # act
    response = client.post(
        f"/sale/delete/", data={f"option-{sale.id}": "delete"}, follow=True
    )

    # assert
    assert response.status_code == 200
    assert "sales/top.html" in response.template_name
    assert Sale.objects.count() == 1


def test_delete_with_wrong_data(client):
    response = client.post(f"/sale/delete/", data={f"option-0": "delete"}, follow=True)

    assert response.status_code == 200
    assert "みかん" in response.content.decode("utf-8")


def test_upload_submit(client):
    with open("tests/upload.csv") as fr:
        response = client.post("/sale/", data={"file": fr}, follow=True)

    assert response.status_code == 200
    assert "2020/11/11 11:11" in response.content.decode("utf-8")
    assert "2021/13/11 11:11" not in response.content.decode("utf-8")
    assert "2022/11/11 11:11" not in response.content.decode("utf-8")
    assert "2023/12/11 11:11" not in response.content.decode("utf-8")
