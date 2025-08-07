from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()

class UserTests(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('users:register')
        self.token_url = reverse('users:login')
        self.refresh_url = reverse('users:token_refresh')
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123@",
            "password2": "test123@"
        }

    def test_user_registration_missing_fields(self):
        response = self.client.post(self.register_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
        self.assertIn("password2", response.data)

    
    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())
    
    def test_user_registration_password_mismatch(self):
        data = self.user_data.copy()
        data["password2"] = "wrongpassword"
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_obtain_missing_fields(self):
        response = self.client.post(self.token_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)
    
    def test_token_refresh_missing_token(self):
        response = self.client.post(self.refresh_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("refresh", response.data)
    
    def test_token_obtain_and_refresh(self):
        self.client.post(self.register_url, self.user_data, format='json')

        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.token_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        refresh_data = {
            "refresh": response.data["refresh"]
        }
        refresh_response = self.client.post(self.refresh_url, refresh_data, format="json")
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)
