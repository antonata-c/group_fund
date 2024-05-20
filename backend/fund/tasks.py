from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_email_task(data, is_html=True):
    """Задача отправки email.

    Args:
        data (dict): Данные для отправки email.
        is_html (bool): Флаг использования html в теле письма.
    """
    message = EmailMultiAlternatives(**data)
    if is_html:
        message.attach_alternative(data["body"], "text/html")
    message.send()
