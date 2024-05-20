from django.conf import settings
from django.http import HttpResponse
from django.template import (
    Context,
    Template
)
from rest_framework import status
from rest_framework.response import Response

from fund.models import EmailTemplate
from fund.tasks import send_email_task


def send_email(recipient_list, context, from_email=None):
    """Отправка email.

    Args:
        recipient_list (list): Список email адресов.
        context (dict): Контекст для шаблона.
        from_email (str): Email отправителя.
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    if not EmailTemplate.objects.filter(is_active=True).exists():
        return
    email_template = EmailTemplate.objects.get(is_active=True)
    message_data = {
        "subject": Template(email_template.subject).render(Context(context)),
        "body": Template(email_template.body).render(Context(context)),
        "from_email": from_email,
        "to": recipient_list,
    }
    send_email_task.delay(message_data, is_html=email_template.is_html)
