from rest_framework.test import APITestCase # type: ignore
from django.urls import reverse
from rest_framework import status # type: ignore
from user.models import *
from django.utils import timezone

class UserLoginActivityTests(APITestCase):
    def test_create_login_activity(self):
        url = reverse('users:login-activity')
        data = {
            'username': 'testuser',
            'status': 'S'
        }
        headers = {
            'HTTP_USER_AGENT': 'Mozilla/5.0',  # Add a valid user agent
            'REMOTE_ADDR': '127.0.0.1'
        }
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserLoginActivity.objects.count(), 1)
        self.assertEqual(UserLoginActivity.objects.first().user_agent_info, 'Mozilla/5.0')

class UserActivityTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        UserActivity1.objects.create(
            user=self.user,
            date=timezone.now(),
            page_visited='Home',
            time_spent='00:05:00'
        )

    def test_get_user_activity(self):
        url = reverse('users:user-activity', args=['testuser'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)