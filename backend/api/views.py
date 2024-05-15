from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, permissions

from api.serializers import (
    CollectCreateSerializer, CollectReadSerializer,
    PaymentCreateSerializer, PaymentReadSerializer,
)
from api.permissions import StaffOrAuthorOrReadOnly
from fund.models import Collect, Payment


class CollectViewSet(viewsets.ModelViewSet):
    """Представление для сборов."""

    queryset = Collect.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = (StaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            return Collect.objects.select_related(
                'author'
            ).prefetch_related(
                'payments'
            ).annotate(
                number_of_donors=Count('payments', distinct=True)
            )
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CollectCreateSerializer
        return CollectReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # @method_decorator(cache_page(60 * 2))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    """Представление для платежей."""

    queryset = Payment.objects.select_related(
        'user', 'collect'
    )
    http_method_names = ['get', 'post']
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        return PaymentReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Token a2586e7a43c2da38c0ed1a33b6bd456002a1f473
    # @method_decorator(cache_page(60 * 2))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
# TODO: вынести константы, расширить документацию, ридми, докер, отправка писем

