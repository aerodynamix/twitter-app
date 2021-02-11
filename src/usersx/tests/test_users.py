from django.test import TestCase, Client
from usersx.models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="test-user-goldman", password="testusergoldman", \
                            city="New Delhi")

    def test_create(self):
        self.assertEqual("New Delhi", User.objects.get(username="test-user-goldman").city)

    def test_api_login(self):
        client = Client()
        response = client.post('/login/', {'username':'test-user-smith'}, format='json')
        self.assertEqual(200, response.status_code)
