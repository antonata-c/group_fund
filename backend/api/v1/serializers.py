from django.utils import timezone
from rest_framework import serializers

from fund.models import (
    Collect,
    EmailTemplate,
    Payment
)


class BaseSerializer(serializers.ModelSerializer):
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть больше нуля.")
        return value


class PaymentShortSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого отображения платежа."""

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Payment
        fields = ("user", "amount", "comment", "hide_amount", "created_at")


class CollectCreateSerializer(BaseSerializer):
    """Сериализатор для создания сбора."""

    class Meta:
        model = Collect
        fields = (
            "title",
            "reason",
            "description",
            "amount",
            "image",
            "end_date",
        )

    def validate_end_date(self, value):
        if value is not None and value < timezone.now():
            raise serializers.ValidationError(
                "Дата окончания сбора не может быть раньше текущей даты."
            )
        return value


class CollectReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения сбора."""

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    number_of_donors = serializers.IntegerField()
    current_amount = serializers.IntegerField()
    payments = PaymentShortSerializer(many=True, read_only=True)

    class Meta:
        model = Collect
        fields = "__all__"


class PaymentCreateSerializer(BaseSerializer):
    """Сериализатор для создания платежа."""

    class Meta:
        model = Payment
        fields = (
            "collect",
            "amount",
            "comment",
            "hide_amount",
        )


class PaymentReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения платежа."""

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    collect = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"


class EmailTemplateSerializer(serializers.ModelSerializer):
    """Сериализатор для шаблонов писем."""

    class Meta:
        model = EmailTemplate
        fields = "__all__"
