from django.contrib.auth import get_user_model
from django.db import models

from .constants import (
    DEFAULT_EMAIL_SUBJECT,
    MAX_DECIMAL_DIGITS,
    MAX_DECIMAL_PLACES,
    MAX_STRING_LENGTH,
    SHORT_STRING_LENGTH
)

User = get_user_model()


class Collect(models.Model):
    """Модель для сборов."""

    class Reason(models.TextChoices):
        BIRTHDAY = "BD", "День рождения"
        WEDDING = "WD", "Свадьба"
        TREATMENT = "TR", "Лечение"
        OTHER = "OT", "Другое"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="collects"
    )
    title = models.CharField(max_length=MAX_STRING_LENGTH)
    reason = models.CharField(
        max_length=MAX_STRING_LENGTH,
        choices=Reason.choices,
        default=Reason.OTHER,
    )
    description = models.TextField()
    amount = models.DecimalField(
        max_digits=MAX_DECIMAL_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=None,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="collect_images/", blank=True)
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = "Сбор"
        verbose_name_plural = "Сборы"

    def __str__(self):
        return self.title[:SHORT_STRING_LENGTH]


class Payment(models.Model):
    """Модель для платежей."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=MAX_DECIMAL_DIGITS, decimal_places=MAX_DECIMAL_PLACES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    hide_amount = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        default_related_name = "payments"


class EmailTemplate(models.Model):
    """Модель для шаблонов писем."""

    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=255, default=DEFAULT_EMAIL_SUBJECT)
    body = models.TextField()
    is_html = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-is_active", "name"]
        verbose_name = "Шаблон письма"
        verbose_name_plural = "Шаблоны писем"

    def __str__(self):
        return f"{'[x] ' if self.is_active else ''}{self.name}"
