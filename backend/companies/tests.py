from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Company
from django.urls import reverse

User = get_user_model()

class CompanyViewSetTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass', email='admin@test.com')
        self.user = User.objects.create_user(username='normal', password='userpass')

        self.company = Company.objects.create(symbol='AAPL', scripcode='5001', company_name='Apple Inc.')

        self.client = APIClient()
        self.url = '/api/companies/'

        # JWT login for superuser
        response = self.client.post(reverse('users:login'), {
            'username': 'admin',
            'password': 'adminpass'
        }, format='json')
        self.superuser_token = response.data['access']

        # JWT login for normal user
        response = self.client.post(reverse('users:login'), {
            'username': 'normal',
            'password': 'userpass'
        }, format='json')
        self.user_token = response.data['access']
    
    def test_list_companies(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_search(self):
        response = self.client.get(self.url, {'search': 'AAPL'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

    def test_create_company_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        data = {'symbol': 'GOOG', 'scripcode': '5002', 'company_name': 'Google LLC'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_company_as_normal_user_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        data = {'symbol': 'MSFT', 'scripcode': '5003', 'company_name': 'Microsoft'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_company_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        response = self.client.patch(f'{self.url}{self.company.id}/', {'company_name': 'Apple Corporation'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company_name'], 'Apple Corporation')

    def test_delete_company_as_normal_user_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.delete(f'{self.url}{self.company.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
