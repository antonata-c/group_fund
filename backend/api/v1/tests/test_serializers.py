from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from api.v1.serializers import (
    CollectCreateSerializer,
    PaymentCreateSerializer
)
from fund.models import (
    Collect,
    User
)


class CollectCreateSerializerTest(TestCase):
    """Тесты для сериализатора CollectCreateSerializer."""

    def setUp(self):
        self.user = User.objects.create(username="testuser")

    def test_valid_collect_data(self):
        """Тест валидных данных для создания сбора."""
        collect_data = {
            "user": self.user.id,
            "title": "Тестовый сбор",
            "reason": Collect.Reason.BIRTHDAY,
            "description": "Тестовое описание",
            "amount": 1000,
            "end_date": timezone.now() + timedelta(days=7),
        }
        serializer = CollectCreateSerializer(data=collect_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_collect_data(self):
        """Тест невалидных данных для создания сбора."""
        collect_data = {
            "user": self.user.id,
            "title": "Тестовый сбор",
            "reason": Collect.Reason.BIRTHDAY,
            "description": "Тестовое описание",
            "amount": 1000,
            "end_date": timezone.now() - timedelta(days=7),
        }
        serializer = CollectCreateSerializer(data=collect_data)
        self.assertFalse(serializer.is_valid())


class PaymentCreateSerializerTest(TestCase):
    """Тесты для сериализатора PaymentCreateSerializer."""

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.collect = Collect.objects.create(
            user=self.user,
            title="Test Collect",
            reason=Collect.Reason.BIRTHDAY,
            description="Test Description",
            amount=1000,
            end_date=timezone.now() + timedelta(days=7),
        )

    def test_valid_payment_data(self):
        """Тест валидных данных для создания платежа."""
        payment_data = {
            "collect": self.collect.id,
            "amount": 500,
        }
        serializer = PaymentCreateSerializer(data=payment_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_payment_data(self):
        """Тест невалидных данных для создания платежа."""
        payment_data = {
            "collect": self.collect.id,
            "amount": -500,
        }
        serializer = PaymentCreateSerializer(data=payment_data)
        self.assertFalse(serializer.is_valid())
