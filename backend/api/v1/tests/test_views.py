from datetime import timedelta
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from fund.models import (
    Collect,
    EmailTemplate,
    Payment,
    User,
)


class CollectViewSetTest(APITestCase):
    """Тесты для представления CollectViewSet."""

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.client.force_authenticate(user=self.user)
        self.collect_data = {
            "title": "Тестовый сбор",
            "reason": Collect.Reason.BIRTHDAY,
            "description": "Тестовое описание",
            "amount": 1000,
            "end_date": timezone.now() + timedelta(days=7),
        }
        self.list_url = reverse("collect-list")

    def test_get_collect_list(self):
        """Тест получения списка сборов."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("api.v1.utils.send_email_task")
    def test_create_collect(self, mock_send_email):
        """Тест создания сбора."""
        objects_count = Collect.objects.count()
        response = self.client.post(
            self.list_url, self.collect_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collect.objects.count(), objects_count + 1)
        self.assertEqual(
            Collect.objects.last().title, self.collect_data["title"]
        )

    def test_create_collect_without_auth(self):
        """Тест создания сбора без аутентификации."""
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.list_url, self.collect_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_collect_with_invalid_data(self):
        """Тест создания сбора с неверными данными."""
        self.collect_data["end_date"] = timezone.now() - timedelta(days=7)
        response = self.client.post(
            self.list_url, self.collect_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PaymentViewSetTest(APITestCase):
    """Тесты для представления PaymentViewSet."""

    def setUp(self):
        self.user = User.objects.create(
            username="testuser", email="anton_ata@mail.ru"
        )
        self.client.force_authenticate(user=self.user)
        self.collect = Collect.objects.create(
            user=self.user,
            title="Тестовый сбор",
            reason=Collect.Reason.BIRTHDAY,
            description="Тестовое описание",
            amount=1000,
            end_date=timezone.now() + timedelta(days=7),
        )
        self.payment_data = {
            "collect": self.collect.id,
            "amount": 500,
        }
        self.list_url = reverse("payment-list")

    def test_get_payment_list(self):
        """Тест получения списка платежей."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("api.v1.utils.send_email_task")
    def test_create_payment(self, mock_send_email):
        """Тест создания платежа."""
        objects_count = Payment.objects.count()
        response = self.client.post(
            self.list_url, self.payment_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), objects_count + 1)
        self.assertEqual(
            Payment.objects.last().amount, self.payment_data["amount"]
        )

    def test_create_payment_without_auth(self):
        """Тест создания платежа без аутентификации."""
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.list_url, self.payment_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_payment_with_invalid_data(self):
        """Тест создания платежа с неверными данными."""
        self.payment_data["amount"] = -10
        response = self.client.post(
            self.list_url, self.payment_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmailTemplateViewSetTest(APITestCase):
    """Тесты для представления EmailTemplateViewSet."""

    def setUp(self):
        self.admin = User.objects.create(username="testuser", is_staff=True)
        self.client.force_authenticate(user=self.admin)
        self.template_data = {
            "name": "Тестовый шаблон",
            "body": "<h1>Тестовое сообщение</h1>",
        }
        self.list_url = reverse("email_template-list")

    def test_get_template_list(self):
        """Тест получения списка шаблонов."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_template(self):
        """Тест создания шаблона."""
        objects_count = EmailTemplate.objects.count()
        response = self.client.post(
            self.list_url, self.template_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmailTemplate.objects.count(), objects_count + 1)
        self.assertEqual(
            EmailTemplate.objects.last().name, self.template_data["name"]
        )

    def test_create_template_without_auth(self):
        """Тест создания шаблона без прав администратора."""
        self.client.force_authenticate(
            user=User.objects.create(username='testuser1')
        )
        response = self.client.post(
            self.list_url, self.template_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_template_with_invalid_data(self):
        """Тест создания шаблона с неверными данными."""
        self.template_data["body"] = ""
        response = self.client.post(
            self.list_url, self.template_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
