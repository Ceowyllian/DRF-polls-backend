import logging

from django.contrib.auth import get_user_model

if __name__ == "__main__":
    import os

    import django

    os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
    django.setup()

import string
import warnings
from random import choice as random_choice
from random import randint

from django_seed import Seed
from faker import Faker
from faker.providers import date_time, profile

from polls.models import Choice, Question

USERS = 4
QUESTIONS = 7
CHOICES = 14
VOTES = 20

User = get_user_model()


def random_ascii_string(length: int, alphabet=string.digits + string.ascii_letters):
    return "".join(random_choice(alphabet) for _ in range(length))


def set_valid_user_passwords():
    credentials = dict()
    for user in User.objects.all():
        password = random_ascii_string(20)
        user.set_password(password)
        user.save()
        credentials[user.username] = password
    return credentials


def run(seed=randint(0, 99999), supress_warnings=False, show_users=False):
    Faker.seed(seed)
    fake = Faker()
    fake.add_provider(date_time)
    fake.add_provider(profile)
    seeder = Seed.seeder()

    seeder.add_entity(
        User,
        USERS,
        {
            "username": lambda x: random_ascii_string(12),
            "password": lambda x: "blank",
            "is_superuser": lambda x: False,
            "is_staff": lambda x: False,
            "is_active": lambda x: True,
        },
    )
    seeder.add_entity(
        Question,
        QUESTIONS,
        {
            "pub_date": fake.date_time_between("-4d", "now"),
        },
    )
    seeder.add_entity(Choice, CHOICES)

    if supress_warnings:
        logger = logging.getLogger()
        logger.disabled = True
        warnings.simplefilter("ignore")
    seeder.execute()

    credentials = set_valid_user_passwords()
    if show_users:
        print("Created users (username --- password):")
        for username, password in credentials.items():
            print(f"{username} --- {password}")


if __name__ == "__main__":
    run(supress_warnings=True)
