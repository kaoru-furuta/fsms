from django.contrib.auth.models import User
from django.test import Client, TestCase


class CoreTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.create_user('test_user'))

    def test_top(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/top.html')

    def test_top_with_no_login(self):
        client = Client()
        response = client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login(self):
        user = User.objects.create_user('test_login_user')
        user.set_password('password')
        user.save()

        client = Client()
        response = client.post('/login/', data={
            'username': 'test_login_user',
            'password': 'password'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/top.html')

    def test_login_with_wrong_data(self):
        user = User.objects.create_user('test_login_user')
        user.set_password('password')
        user.save()

        client = Client()
        response = client.post('/login/', data={
            'username': 'test_login_user',
            'password': 'wrong_password'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
