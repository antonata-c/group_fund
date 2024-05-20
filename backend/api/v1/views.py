from django.db.models import (
    Count,
    Sum
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import (
    permissions,
    viewsets
)

from api.v1.permissions import StaffOrAuthorOrReadOnly
from api.v1.serializers import (
    CollectCreateSerializer,
    CollectReadSerializer,
    EmailTemplateSerializer,
    PaymentCreateSerializer,
    PaymentReadSerializer
)
from api.v1.utils import send_email
from fund.models import (
    Collect,
    EmailTemplate,
    Payment
)


class BaseViewSet(viewsets.ModelViewSet):
    """Базовое представление."""

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        send_email(
            recipient_list=[user.email],
            context={
                "event": "сбор" if self.basename == "collect" else "платеж",
                "amount": serializer.validated_data.get("amount"),
            },
        )


class CollectViewSet(BaseViewSet):
    """Представление для сборов."""

    queryset = Collect.objects.all()
    http_method_names = ["get", "post"]
    permission_classes = (StaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return (
                Collect.objects.select_related("user")
                .prefetch_related("payments")
                .annotate(
                    number_of_donors=Count("payments__user", distinct=True),
                    current_amount=Sum("payments__amount"),
                )
                .order_by("id")
            )
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CollectCreateSerializer
        return CollectReadSerializer


class PaymentViewSet(BaseViewSet):
    """Представление для платежей."""

    queryset = Payment.objects.select_related("user", "collect").order_by("id")
    http_method_names = ["get", "post"]
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PaymentCreateSerializer
        return PaymentReadSerializer


class EmailTemplateViewSet(viewsets.ModelViewSet):
    """Представление для шаблонов писем."""

    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = (permissions.IsAdminUser,)

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
