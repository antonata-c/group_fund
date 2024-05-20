import factory
from django.utils import timezone

from .models import Collect, Payment, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")


class CollectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collect

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence")
    reason = factory.Faker(
        "random_element", elements=[choice[0] for choice in Collect.Reason.choices]
    )
    description = factory.Faker("paragraph")
    planned_amount = factory.Faker("random_number", digits=4)
    end_date = factory.Faker(
        "future_datetime", end_date="+30d", tzinfo=timezone.now().tzinfo
    )


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory(UserFactory)
    collect = factory.SubFactory(CollectFactory)
    amount = factory.Faker("random_number", digits=3)
    created_at = factory.Faker("date_time_this_month")
    comment = factory.Faker("sentence")
    hide_amount = factory.Faker("boolean")
