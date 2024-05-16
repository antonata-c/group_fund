from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, viewsets

from api.permissions import StaffOrAuthorOrReadOnly
from api.serializers import (CollectCreateSerializer, CollectReadSerializer,
                             PaymentCreateSerializer, PaymentReadSerializer)
from fund.models import Collect, Payment
from fund.tasks import send_email_task


class BaseViewSet(viewsets.ModelViewSet):
    """Базовое представление."""

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        event = "сбор" if self.basename == 'Collect' else "платеж"
        send_email_task.delay(
            subject=f'Новый {event}.',
            message=f'Был добавлен новый {event}.',
            recipient_list=[self.request.user.email]
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
                number_of_donors=Count('payments__user', distinct=True)
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
