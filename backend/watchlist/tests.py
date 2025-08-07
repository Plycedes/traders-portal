from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from companies.models import Company
from watchlist.models import WatchList
from rest_framework_simplejwt.tokens import RefreshToken

class WatchlistTests(APITestCase):

    def setUp(self):
        # Create test user and generate JWT token
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_header = f'Bearer {self.token}'

        # Create a test company
        self.company = Company.objects.create(company_name='Test Company', symbol='TEST', scripcode='12345')

        # URLs
        self.watchlist_url = reverse('watchlist:watchlist-list')
        self.add_url = reverse('watchlist:watchlist-add')
        self.remove_url = reverse('watchlist:watchlist-remove')

    def test_add_to_watchlist(self):
        response = self.client.post(
            self.add_url,
            data={'company_id': self.company.id},
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(WatchList.objects.filter(user=self.user, company=self.company).exists())

    def test_add_same_company_twice(self):
        WatchList.objects.create(user=self.user, company=self.company)
        response = self.client.post(
            self.add_url,
            data={'company_id': self.company.id},
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WatchList.objects.filter(user=self.user, company=self.company).count(), 1)

    def test_remove_from_watchlist(self):
        WatchList.objects.create(user=self.user, company=self.company)
        response = self.client.post(
            self.remove_url,
            data={'company_id': self.company.id},
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(WatchList.objects.filter(user=self.user, company=self.company).exists())

    def test_remove_nonexistent_watchlist_entry(self):
        response = self.client.post(
            self.remove_url,
            data={'company_id': self.company.id},
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Already removed from watchlist or was never added')

    def test_list_watchlist(self):
        WatchList.objects.create(user=self.user, company=self.company)
        response = self.client.get(
            self.watchlist_url,
            HTTP_AUTHORIZATION=self.auth_header
        )        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

