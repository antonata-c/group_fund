from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone
from fund.models import Collect, Payment, User


class CollectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.collect = Collect.objects.create(
            user=self.user,
            title="Тестовый сбор",
            reason=Collect.Reason.BIRTHDAY,
            description="Тестовое описание",
            planned_amount=1000,
            image="path/to/image.jpg",
            end_date=timezone.now() + timedelta(days=7),
        )

    def test_collect_creation(self):
        self.assertEqual(self.collect.title, "Тестовый сбор")
        self.assertEqual(self.collect.reason, Collect.Reason.BIRTHDAY)
        self.assertEqual(self.collect.description, "Тестовое описание")
        self.assertEqual(self.collect.planned_amount, 1000)
        self.assertTrue(isinstance(self.collect.end_date, datetime))
        self.assertEqual(self.collect.user, self.user)
        self.assertEqual(self.collect.image, "path/to/image.jpg")


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.collect = Collect.objects.create(
            user=self.user,
            title="Тестовый сбор",
            reason=Collect.Reason.BIRTHDAY,
            description="Тестовое описание",
            planned_amount=1000,
            end_date=timezone.now() + timedelta(days=7),
        )
        self.payment = Payment.objects.create(
            user=self.user, collect=self.collect, amount=500
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.collect, self.collect)
        self.assertEqual(self.payment.amount, 500)
