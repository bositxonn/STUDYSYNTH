from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('users:my-profile')

    def test_get_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if profile was automatically created
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['courses_enrolled'], 0)
