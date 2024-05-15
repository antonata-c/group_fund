from django.db import models
from django.contrib.auth.models import User


class Collect(models.Model):
    """Модель для сборов."""

    class Reason(models.TextChoices):
        BIRTHDAY = 'BD', 'День рождения'
        WEDDING = 'WD', 'Свадьба'
        TREATMENT = 'TR', 'Лечение'
        OTHER = 'OT', 'Другое'

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collects'
    )
    title = models.CharField(max_length=255)
    reason = models.CharField(
        max_length=255, choices=Reason.choices, default=Reason.OTHER
    )
    description = models.TextField()
    planned_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=None, null=True, blank=True
    )
    current_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    image = models.ImageField(
        upload_to='collect_images/', blank=True
    )
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'

    def __str__(self):
        return self.title[:15]


class Payment(models.Model):
    """Модель для платежей."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    hide_amount = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        default_related_name = 'payments'

    def __str__(self):
        return f'{self.user.username} - {self.collect.title}'
