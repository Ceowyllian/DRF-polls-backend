if __name__ == '__main__':
    import os
    import django

    os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
    django.setup()

import warnings
from random import randint

from django_seed import Seed
from faker import Faker
from faker.providers import date_time

from polls.models import Question, Choice
from uuid import uuid4


def run(seed=randint(0, 99999)):
    Faker.seed(seed)
    fake = Faker()
    fake.add_provider(date_time)
    seeder = Seed.seeder()
    seeder.add_entity(Question, 3, {
        'pub_date': fake.date_time_between('-4d', 'now'),
    })
    seeder.add_entity(Choice, 10, {
        'choice_uuid': lambda x: uuid4(),
        'votes': lambda x: randint(0, 50),
    })
    seeder.execute()


if __name__ == '__main__':
    warnings.simplefilter('ignore')
    run()
