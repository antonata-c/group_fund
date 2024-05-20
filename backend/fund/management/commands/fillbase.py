from django.core.management.base import BaseCommand
from faker import Faker

from fund.factories import (
    CollectFactory,
    PaymentFactory,
    UserFactory
)
from fund.models import EmailTemplate

fake = Faker()


class Command(BaseCommand):
    """Класс команды для наполнения базы данных тестовыми данными."""

    help = "Создает тестовые данные для наполнения базы данных."

    def add_arguments(self, parser):
        """Добавление аргументов в команду."""
        parser.add_argument(
            "--users", type=int, default=30, help="Количество пользователей"
        )
        parser.add_argument(
            "--collects",
            type=int,
            default=10,
            help="Количество сборов на пользователя",
        )
        parser.add_argument(
            "--payments",
            type=int,
            default=15,
            help="Количество платежей на сбор",
        )

    def handle(self, *args, **kwargs):
        """Заполнение базы данных тестовыми данными."""
        num_users = kwargs["users"]
        num_collects_per_user = kwargs["collects"]
        num_payments_per_collect = kwargs["payments"]

        users = UserFactory.create_batch(num_users)

        for user in users:
            collects = CollectFactory.create_batch(
                num_collects_per_user, user=user
            )
            for collect in collects:
                PaymentFactory.create_batch(
                    num_payments_per_collect, user=user, collect=collect
                )
        EmailTemplate.objects.create(
            name="Базовый шаблон",
            body="<h1>Благодарим за создание {{ event }}а!</h1>"
            "<p>Будем ждать вас снова на нашем портале.</p>",
        ),
        EmailTemplate.objects.create(
            name="Новый шаблон",
            body="<h1>Мы рады, что вы с нами!</h1>"
            "<p>Ваш {{ event }} успешно создан.</p>",
        ),

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены."))
