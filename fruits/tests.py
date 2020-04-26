from django.contrib.auth.models import User
from django.test import Client, TestCase


class FruitTest(TestCase):
    fixtures = ["fruits.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.create_user("test_user"))

    def test_top(self):
        response = self.client.get("/fruit/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fruits/top.html")
        self.assertContains(response=response, text="みかん")

    def test_top_with_no_login(self):
        client = Client()

        response = client.get("/fruit/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_new(self):
        response = self.client.get("/fruit/new/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fruits/form.html")

    def test_new_with_no_login(self):
        client = Client()

        response = client.get("/fruit/new/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_new_submit(self):
        response = self.client.post(
            "/fruit/new/", data={"name": "りんご", "price": 200}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fruits/top.html")
        self.assertContains(response=response, text="りんご")

    def test_new_submit_with_no_login(self):
        client = Client()

        response = client.post(
            "/fruit/new/", data={"name": "りんご", "price": 200}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_new_submit_with_wrong_data(self):
        response = self.client.post(
            "/fruit/new/", data={"name": "みかん", "price": "foo"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fruits/form.html")

    def test_edit(self):
        response = self.client.get("/fruit/1/edit/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fruits/form.html")

    def test_edit_with_no_login(self):
        client = Client()

        response = client.get("/fruit/1/edit/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_edit_submit(self):
        response = self.client.post(
            "/fruit/1/edit/", data={"name": "りんご", "price": 200}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fruits/top.html")
        self.assertContains(response=response, text="りんご")

    def test_edit_submit_with_no_login(self):
        client = Client()

        response = client.post(
            "/fruit/1/edit/", data={"name": "りんご", "price": 200}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_edit_submit_with_wrong_data(self):
        response = self.client.post(
            "/fruit/1/edit/", data={"name": "りんご", "price": "foo"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fruits/form.html")

    def test_delete_submit(self):
        response = self.client.post("/fruit/1/delete/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fruits/top.html")
        self.assertNotContains(response=response, text="みかん")

    def test_delete_with_no_login(self):
        client = Client()

        response = client.post("/fruit/1/delete/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_delete_with_wrong_data(self):
        response = self.client.post("/fruit/2/delete/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fruits/top.html")
        self.assertContains(response=response, text="みかん")
