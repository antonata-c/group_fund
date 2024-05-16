from django.utils import timezone
from rest_framework import serializers

from fund.models import Collect, Payment


class PaymentShortSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого отображения платежа."""

    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Payment
        fields = ('user', 'amount', 'comment', 'hide_amount', 'created_at')


class CollectCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания сбора."""

    class Meta:
        model = Collect
        fields = ('title', 'reason', 'description',
                  'planned_amount', 'image', 'end_date')

    def validate_planned_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Сумма сбора должна быть больше нуля.'
            )
        return value

    def validate_end_date(self, value):
        if value is not None and value < timezone.now():
            raise serializers.ValidationError(
                'Дата окончания сбора не может быть раньше текущей даты.'
            )
        return value


class CollectReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения сбора."""

    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    number_of_donors = serializers.IntegerField()
    current_amount = serializers.IntegerField()
    payments = PaymentShortSerializer(many=True, read_only=True)

    class Meta:
        model = Collect
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания платежа."""

    class Meta:
        model = Payment
        fields = ('collect', 'amount', 'comment', 'hide_amount')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Сумма платежа должна быть больше нуля.'
            )
        return value


class PaymentReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения платежа."""

    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    collect = serializers.SlugRelatedField(
        slug_field='title', read_only=True
    )

    class Meta:
        model = Payment
        fields = '__all__'
