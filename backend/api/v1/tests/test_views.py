from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from fund.models import Collect, Payment, User


class CollectViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.client.force_authenticate(user=self.user)
        self.collect_data = {
            'title': 'Тестовый сбор',
            'reason': Collect.Reason.BIRTHDAY,
            'description': 'Тестовое описание',
            'planned_amount': 1000,
            'end_date': timezone.now() + timedelta(days=7),
        }
        self.list_url = reverse('collect-list')

    def test_get_collect_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_collect(self):
        objects_count = Collect.objects.count()
        response = self.client.post(
            self.list_url, self.collect_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collect.objects.count(), objects_count + 1)
        self.assertEqual(
            Collect.objects.last().title, self.collect_data['title']
        )

    def test_create_collect_without_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.list_url, self.collect_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_collect_with_invalid_data(self):
        self.collect_data['end_date'] = timezone.now() - timedelta(days=7)
        response = self.client.post(
            self.list_url, self.collect_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PaymentViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.client.force_authenticate(user=self.user)
        self.collect = Collect.objects.create(
            user=self.user,
            title='Тестовый сбор',
            reason=Collect.Reason.BIRTHDAY,
            description='Тестовое описание',
            planned_amount=1000,
            end_date=timezone.now() + timedelta(days=7),
        )
        self.payment_data = {
            'collect': self.collect.id,
            'amount': 500,
        }
        self.list_url = reverse('payment-list')

    def test_get_payment_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_payment(self):
        objects_count = Payment.objects.count()
        response = self.client.post(
            self.list_url, self.payment_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), objects_count + 1)
        self.assertEqual(
            Payment.objects.last().amount, self.payment_data['amount']
        )

    def test_create_payment_without_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.list_url, self.payment_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_payment_with_invalid_data(self):
        self.payment_data['amount'] = -10
        response = self.client.post(
            self.list_url, self.payment_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
