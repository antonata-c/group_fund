from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import EmailTemplate


@receiver(pre_save, sender=EmailTemplate)
def make_other_templates_inactive(sender, instance, **kwargs):
    """Сигнал делает все шаблоны неактивными, кроме текущего."""
    if instance.is_active:
        EmailTemplate.objects.filter(is_active=True).update(is_active=False)
