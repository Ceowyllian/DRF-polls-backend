from datetime import datetime

import factory
from django.contrib.auth import get_user_model

__all__ = [
    "UserFactory",
]


class UserFactory(factory.django.DjangoModelFactory):
    password = factory.django.Password("test_password")
    last_login = factory.Faker(
        "date_between_dates",
        date_start=datetime(2023, 1, 1),
        date_end=datetime(2023, 12, 31),
    )
    username = factory.Sequence(lambda n: f"test_user_{n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_staff = factory.LazyAttribute(lambda _: False)
    date_joined = factory.Faker(
        "date_between_dates",
        date_start=datetime(2022, 1, 1),
        date_end=datetime(2022, 12, 31),
    )

    class Meta:
        model = get_user_model()
