from django.core.management import call_command
from django.test import TestCase

from fund.models import (
    Collect,
    Payment,
    User
)


class FillBaseCommandTest(TestCase):
    """Тест на заполнение базы данных тестовыми данными"""
    def test_fill_base_command(self):
        call_command("fillbase", users=5, collects=10, payments=10)
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(Collect.objects.count(), 50)
        self.assertEqual(Payment.objects.count(), 500)
