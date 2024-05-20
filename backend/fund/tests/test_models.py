from datetime import (
    datetime,
    timedelta
)

from django.test import TestCase
from django.utils import timezone

from fund.models import (
    Collect,
    EmailTemplate,
    Payment,
    User
)


class CollectModelTest(TestCase):
    """Тестирование модели Collect."""

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.collect = Collect.objects.create(
            user=self.user,
            title="Тестовый сбор",
            reason=Collect.Reason.BIRTHDAY,
            description="Тестовое описание",
            amount=1000,
            image="path/to/image.jpg",
            end_date=timezone.now() + timedelta(days=7),
        )

    def test_collect_creation(self):
        """Тестирование создания объекта сбора."""
        self.assertEqual(self.collect.title, "Тестовый сбор")
        self.assertEqual(self.collect.reason, Collect.Reason.BIRTHDAY)
        self.assertEqual(self.collect.description, "Тестовое описание")
        self.assertEqual(self.collect.amount, 1000)
        self.assertTrue(isinstance(self.collect.end_date, datetime))
        self.assertEqual(self.collect.user, self.user)
        self.assertEqual(self.collect.image, "path/to/image.jpg")


class PaymentModelTest(TestCase):
    """Тестирование модели Payment."""

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.collect = Collect.objects.create(
            user=self.user,
            title="Тестовый сбор",
            reason=Collect.Reason.BIRTHDAY,
            description="Тестовое описание",
            amount=1000,
            end_date=timezone.now() + timedelta(days=7),
        )
        self.payment = Payment.objects.create(
            user=self.user, collect=self.collect, amount=500
        )

    def test_payment_creation(self):
        """Тестирование создания объекта платежа."""
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.collect, self.collect)
        self.assertEqual(self.payment.amount, 500)


class EmailTemplateModelTest(TestCase):
    """Тестирование модели EmailTemplate."""

    def setUp(self):
        self.email_object = EmailTemplate.objects.create(
            name="Базовый шаблон",
            body="<h1>Благодарим за создание {{ event }}а!</h1>"
            "<p>Будем ждать вас снова на нашем портале.</p>",
        )

    def test_email_template_creation(self):
        """Тестирование создания объекта шаблона письма."""
        self.assertEqual(self.email_object.name, "Базовый шаблон")
        self.assertEqual(self.email_object.is_html, True)

    def test_one_active_template(self):
        """Тестирование наличия только одного активного шаблона."""
        count_before = EmailTemplate.objects.filter(is_active=True).count()
        EmailTemplate.objects.create(
            name="Тестовый шаблон", body="<h1>Тестовый текст</h1>"
        )
        count_after = EmailTemplate.objects.filter(is_active=True).count()
        self.assertEqual(count_before, 1)
        self.assertEqual(count_after, 1)
