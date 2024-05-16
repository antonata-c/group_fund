from django.db.models import Count, Sum
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_page
from rest_framework import permissions, viewsets

from api.v1.permissions import StaffOrAuthorOrReadOnly
from api.v1.serializers import (
    CollectCreateSerializer, CollectReadSerializer,
    PaymentCreateSerializer, PaymentReadSerializer,
)
from fund.models import Collect, Payment
from fund.tasks import send_email_task


class BaseViewSet(viewsets.ModelViewSet):
    """Базовое представление."""

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        if self.basename == 'collect':
            event = "сбор"
            amount = serializer.instance.planned_amount
        else:
            event = "платеж"
            amount = serializer.instance.amount
        context = {
            'event': event,
            'amount': amount,
            'user_name': user.first_name if user.first_name else user.username,
        }
        html_message = render_to_string(
            'email-message.html',
            context=context
        )
        send_email_task.delay(
            subject=f'Новое письмо.',
            message=strip_tags(html_message),
            recipient_list=[user.email],
            html_message=html_message
        )


class CollectViewSet(BaseViewSet):
    """Представление для сборов."""

    queryset = Collect.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = (StaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            return Collect.objects.select_related(
                'user'
            ).prefetch_related(
                'payments'
            ).annotate(
                number_of_donors=Count('payments__user', distinct=True),
                current_amount=Sum('payments__amount')
            ).order_by('id')
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CollectCreateSerializer
        return CollectReadSerializer


class PaymentViewSet(BaseViewSet):
    """Представление для платежей."""

    queryset = Payment.objects.select_related(
        'user', 'collect'
    ).order_by('id')
    http_method_names = ['get', 'post']
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        return PaymentReadSerializer
