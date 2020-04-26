from django.contrib.auth.models import User
from django.test import Client, TestCase


class SummaryTest(TestCase):
    fixtures = ["fruits.json", "sales.json"]

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.create_user("test_user"))

    def test_top(self):
        response = self.client.get("/summary/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "summaries/top.html")
        self.assertContains(response=response, text="みかん")

    def test_top_with_no_login(self):
        client = Client()

        response = client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
