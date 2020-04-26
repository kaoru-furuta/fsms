from django.contrib.auth.models import User
from django.test import Client, TestCase


class FruitTest(TestCase):
    fixtures = ["fruits.json", "sales.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.create_user("test_user"))

    def test_top(self):
        response = self.client.get("/sale/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/top.html")
        self.assertContains(response=response, text="みかん")

    def test_top_with_no_login(self):
        client = Client()

        response = client.get("/sale/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_new(self):
        response = self.client.get("/sale/new/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/form.html")

    def test_new_with_no_login(self):
        client = Client()

        response = client.get("/sale/new/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_new_submit(self):
        response = self.client.post(
            "/sale/new/",
            data={"fruit_list": 1, "number": 1, "sold_at": "2018-12-13T12:13"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/top.html")
        self.assertContains(response=response, text="2018/12/13 12:13")

    def test_new_submit_with_no_login(self):
        client = Client()

        response = client.post(
            "/sale/new/",
            data={"fruit_list": 1, "number": 1, "sold_at": "2018-12-13T12:13"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_new_submit_with_wrong_data(self):
        response = self.client.post(
            "/sale/new/",
            data={"fruit_list": 2, "number": 1, "sold_at": "2018-12-13T12:13"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/form.html")

    def test_edit(self):
        response = self.client.get("/sale/1/edit/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/form.html")

    def test_edit_with_no_login(self):
        client = Client()

        response = client.get("/sale/1/edit/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_edit_submit(self):
        response = self.client.post(
            "/sale/1/edit/",
            data={"fruit_list": 1, "number": 1, "sold_at": "2018-12-14T12:14"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/top.html")
        self.assertContains(response=response, text="2018/12/14 12:14")

    def test_edit_submit_with_no_login(self):
        client = Client()

        response = client.post(
            "/sale/1/edit/",
            data={"fruit_list": 1, "number": 1, "sold_at": "2018-12-14T12:14"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_edit_submit_with_wrong_data(self):
        response = self.client.post(
            "/sale/1/edit/",
            data={"fruit_list": 2, "number": 1, "sold_at": "2018-12-14T12:14"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/form.html")

    def test_delete_submit(self):
        response = self.client.post("/sale/1/delete/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/top.html")
        self.assertNotContains(response=response, text="みかん")

    def test_delete_with_no_login(self):
        client = Client()

        response = client.post("/sale/1/delete/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_delete_with_wrong_data(self):
        response = self.client.post("/sale/2/delete/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/top.html")
        self.assertContains(response=response, text="みかん")

    def test_upload_submit(self):
        with open("sales/fixtures/upload.csv") as fr:
            response = self.client.post(
                "/sale/upload/", data={"file": fr,}, follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/top.html")
        self.assertContains(response=response, text="2020/11/11 11:11")
        self.assertNotContains(response=response, text="2021/13/11 11:11")
        self.assertNotContains(response=response, text="2022/11/11 11:11")
        self.assertNotContains(response=response, text="2023/12/11 11:11")
