from django.db.models.signals import post_save
from django.dispatch import receiver

from fund.models import Collect, Payment


@receiver(post_save, sender=Payment)
def update_model2(sender, instance, created, **kwargs):
    if created:
        collect = Collect.objects.get(id=instance.collect.id)
        collect.current_amount += instance.amount
        collect.save()
