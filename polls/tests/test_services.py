from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, PermissionDenied
from django.test import TestCase

from polls.models import Question, Choice
from . import fixtures
from .fixtures import Q, C
from .. import services

User = get_user_model()


class TestCreateQuestionInstance(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='xavia3k',
            password='3pD5oykYb2sUIZWYMje',
            email='archibald_moreltaq@cups.ws'
        )

    def test_created_successfully(self):
        question_data = fixtures.question()

        question = services.question.create_question_instance(created_by=self.user, **question_data)

        for field, value in question_data.items():
            self.assertEquals(getattr(question, field), value)

    def test_fail_too_short_title(self):
        question_data = fixtures.question(
            title=Q.title.too_short()
        )
        self.unable_to_create(**question_data)

    def test_fail_too_long_title(self):
        question_data = fixtures.question(
            title=Q.title.too_long()
        )
        self.unable_to_create(**question_data)

    def test_fail_too_short_text(self):
        question_data = fixtures.question(
            title=Q.text.too_short()
        )
        self.unable_to_create(**question_data)

    def test_fail_too_long_text(self):
        question_data = fixtures.question(
            title=Q.text.too_long()
        )
        self.unable_to_create(**question_data)

    def unable_to_create(self, **kwargs):
        with self.assertRaises(ValidationError):
            services.question.create_question_instance(created_by=self.user, **kwargs)


class TestCreateChoiceInstances(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='xavia3k',
            password='3pD5oykYb2sUIZWYMje',
            email='archibald_moreltaq@cups.ws'
        )
        cls.question = Question.objects.create(
            **fixtures.question(),
            created_by=cls.user
        )

    def test_created_successfully(self):
        choices = fixtures.choice_list()

        instances = services.question.create_choice_instances(
            question=self.question,
            choices=choices
        )

        self.assertEquals(len(instances), len(choices))
        for choice in instances:
            self.assertIn(choice.text, choices)

    def test_fail_too_many_choices(self):
        choices = fixtures.choice_list(number=C.number.too_many())
        self.unable_to_create(choices)

    def test_fail_too_few_choices(self):
        choices = fixtures.choice_list(number=C.number.too_few())
        self.unable_to_create(choices)

    def test_fail_empty_text_choices(self):
        choices = fixtures.choice_list(text=C.text.empty())
        self.unable_to_create(choices)

    def test_fail_too_long_text_choices(self):
        choices = fixtures.choice_list(text=C.text.too_long())
        self.unable_to_create(choices)

    def test_fail_identical_choices(self):
        choices = fixtures.choice_list(text=C.text.identical())
        self.unable_to_create(choices)

    def unable_to_create(self, choices):
        with self.assertRaises(ValidationError):
            services.question.create_choice_instances(
                question=self.question,
                choices=choices
            )


class TestQuestionDestroy(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='xavia3k',
            password='3pD5oykYb2sUIZWYMje',
            email='archibald_moreltaq@cups.ws'
        )
        cls.question = Question.objects.create(
            **fixtures.question(),
            created_by=cls.user
        )

    def test_destroyed_successfully(self):
        question_pk = self.question.pk

        services.question.destroy(
            question_pk=question_pk,
            destroyed_by=self.user
        )

        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=question_pk)

    def test_fail_question_does_not_exist(self):
        question_pk = -1

        with self.assertRaises(Question.DoesNotExist):
            services.question.destroy(
                question_pk=question_pk,
                destroyed_by=self.user
            )

    def test_fail_permission_denied(self):
        question_pk = self.question.pk
        another_user = User.objects.create_user(
            username='radamesdck7',
            password='fQG2tmyGg7w5s7kbzlD3X2Ht',
            email='constantina_khalildyb@lake.nr'
        )

        with self.assertRaises(PermissionDenied):
            services.question.destroy(
                question_pk=question_pk,
                destroyed_by=another_user
            )


class TestQuestionRetrieve(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='xavia3k',
            password='3pD5oykYb2sUIZWYMje',
            email='archibald_moreltaq@cups.ws'
        )
        cls.question = Question.objects.create(
            **fixtures.question(),
            created_by=cls.user
        )
        cls.choices = [
            Choice.objects.create(text=text, question=cls.question)
            for text in fixtures.choice_list()
        ]

    def test_retrieved_successfully(self):
        question_pk = self.question.pk

        question = services.question.retrieve(question_pk=question_pk)

        self.assertEqual(question, self.question)

    def test_fail_question_does_not_exist(self):
        question_pk = -1

        with self.assertRaises(Question.DoesNotExist):
            question = services.question.retrieve(question_pk=question_pk)


class TestQuestionList(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_user',
            password='3pD5oykYb2sUIZWYMje',
            email='archibald_moreltaq@cups.ws'
        )

    def test_filter_by_created_by(self):
        amount = 3
        for _ in range(amount):
            Question.objects.create(
                **fixtures.question(),
                created_by=self.user
            )

        queryset = services.question.question_list(
            filters={'created_by': self.user.username}
        )

        for question in queryset:
            self.assertEquals(
                question.created_by,
                self.user
            )
        self.assertEquals(len(queryset), amount)

    def test_filter_by_title(self):
        q1 = Question.objects.create(
            title='aaaaaaaaaaaa',
            text='aaaaaaaaaaaa',
            created_by=self.user
        )
        q2 = Question.objects.create(
            title='bbbbbbbbbbb',
            text='bbbbbbbbbbb',
            created_by=self.user
        )

        queryset = services.question.question_list(
            filters={'title': 'aaaa'}
        )

        self.assertIn(q1, queryset)
        self.assertNotIn(q2, queryset)

    def test_filter_by_text(self):
        q1 = Question.objects.create(
            title='aaaaaaaaaaaa',
            text='aaaaaaaaaaaa',
            created_by=self.user
        )
        q2 = Question.objects.create(
            title='bbbbbbbbbbb',
            text='bbbbbbbbbbb',
            created_by=self.user
        )

        queryset = services.question.question_list(
            filters={'text': 'aaaa'}
        )

        self.assertIn(q1, queryset)
        self.assertNotIn(q2, queryset)

    def test_filter_by_date_before(self):
        q1 = Question.objects.create(
            **fixtures.question(),
            created_by=self.user,
            pub_date=datetime(year=2022, month=12, day=4)
        )
        q2 = Question.objects.create(
            **fixtures.question(),
            created_by=self.user,
            pub_date=datetime(year=2022, month=12, day=10)
        )

        queryset = services.question.question_list(
            filters={'date_before': '2022-12-9'}
        )

        self.assertIn(q1, queryset)
        self.assertNotIn(q2, queryset)

    def test_filter_by_date_after(self):
        q1 = Question.objects.create(
            **fixtures.question(),
            created_by=self.user,
            pub_date=datetime(year=2022, month=12, day=4)
        )
        q2 = Question.objects.create(
            **fixtures.question(),
            created_by=self.user,
            pub_date=datetime(year=2022, month=12, day=10)
        )

        queryset = services.question.question_list(
            filters={'date_after': '2022-12-5'}
        )

        self.assertIn(q2, queryset)
        self.assertNotIn(q1, queryset)
