from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, PermissionDenied
from django.test import TestCase

from polls.models import (
    Question,
    Choice,
    Vote,
)
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
            username='test_user', password='3pD5oykYb2s',
            email='archibald_moreltaq@cups.ws'
        )

    def test_filter_by_created_by(self):

        # Questions that MUST appear in the results
        expected_questions = set()
        for _ in range(3):
            expected_questions.add(
                Question.objects.create(
                    created_by=self.user, **fixtures.question())
            )

        another_user = User.objects.create_user(
            username='rakeshap', password='24dQdzXxH13a',
            email='tawan_brayr@hiv.bxu'
        )
        # Questions that SHOULD NEVER appear in the results
        unsuitable_questions = set()
        for _ in range(5):
            unsuitable_questions.add(
                Question.objects.create(
                    created_by=another_user, **fixtures.question())
            )

        results = services.question.question_list(
            filters={'created_by': self.user.username}
        )

        self.assertEquals(len(results), len(expected_questions))

        for question in results:
            self.assertEquals(question.created_by, self.user)

        for question in expected_questions:
            self.assertIn(question, results)

        for question in unsuitable_questions:
            self.assertNotIn(question, results)

    def test_filter_by_title(self):
        # Questions that MUST appear in the results
        expected_questions = set()
        for _ in range(5):
            expected_questions.add(
                Question.objects.create(
                    title='aaaa', text='blablabla',
                    created_by=self.user)
            )

        # Questions that SHOULD NEVER appear in the results
        unsuitable_questions = set()
        for _ in range(5):
            unsuitable_questions.add(
                Question.objects.create(
                    title='bbbb', text='blablabla',
                    created_by=self.user)
            )

        results = services.question.question_list(
            filters={'title': 'aaaa'}
        )

        self.assertEquals(len(results), len(expected_questions))

        for question in results:
            self.assertEquals(question.created_by, self.user)

        for question in expected_questions:
            self.assertIn(question, results)

        for question in unsuitable_questions:
            self.assertNotIn(question, results)

    def test_filter_by_text(self):
        # Questions that MUST appear in the results
        expected_questions = set()
        for _ in range(5):
            expected_questions.add(
                Question.objects.create(
                    title='blablabla', text='aaaa',
                    created_by=self.user)
            )

        # Questions that SHOULD NEVER appear in the results
        unsuitable_questions = set()
        for _ in range(5):
            unsuitable_questions.add(
                Question.objects.create(
                    title='blablabla', text='bbbb',
                    created_by=self.user)
            )

        results = services.question.question_list(
            filters={'text': 'aaaa'}
        )

        self.assertEquals(len(results), len(expected_questions))

        for question in results:
            self.assertEquals(question.created_by, self.user)

        for question in expected_questions:
            self.assertIn(question, results)

        for question in unsuitable_questions:
            self.assertNotIn(question, results)

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


class TestPerformVote(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_user',
            password='3pD5oykYb2sUIZWYMje',
            email='archibald_moreltaq@cups.ws'
        )
        cls.question = Question.objects.create(
            **fixtures.question(),
            created_by=cls.user,
        )
        cls.choice_1 = Choice.objects.create(
            text='foo',
            question=cls.question
        )
        cls.choice_2 = Choice.objects.create(
            text='bar',
            question=cls.question
        )

    def test_perform_vote_successfully(self):
        self.assertEqual(self.choice_1.vote_set.count(), 0)

        services.vote.perform_vote(
            choice_pk=self.choice_1.pk,
            user=self.user
        )

        self.assertEqual(self.choice_1.vote_set.count(), 1)

    def test_fail_to_vote_twice_for_the_same_choice(self):
        Vote.objects.create(
            voted_by=self.user,
            question=self.question,
            choice=self.choice_1,
        )

        with self.assertRaises(ValidationError):
            services.vote.perform_vote(
                choice_pk=self.choice_1.pk,
                user=self.user
            )

    def test_fail_to_vote_twice_for_the_same_question(self):
        Vote.objects.create(
            voted_by=self.user,
            question=self.question,
            choice=self.choice_1,
        )

        with self.assertRaises(ValidationError):
            services.vote.perform_vote(
                choice_pk=self.choice_2.pk,
                user=self.user
            )


class TestCancelVote(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_user',
            password='3pD5oykYb2sUIZWYMje',
            email='archibald_moreltaq@cups.ws'
        )
        cls.question = Question.objects.create(
            **fixtures.question(),
            created_by=cls.user,
        )
        cls.choice = Choice.objects.create(
            text='foo',
            question=cls.question
        )
        cls.vote = Vote.objects.create(
            voted_by=cls.user,
            question=cls.question,
            choice=cls.choice,
        )

    def test_cancel_vote_successfully(self):
        self.assertEquals(self.choice.vote_set.count(), 1)

        services.vote.cancel_vote(
            choice_pk=self.choice.pk,
            user=self.user
        )

        self.assertEquals(self.choice.vote_set.count(), 0)

    def test_fail_user_did_not_vote(self):
        self.vote.delete()
        self.assertEquals(self.choice.vote_set.count(), 0)

        with self.assertRaises(ValidationError):
            services.vote.cancel_vote(
                choice_pk=self.choice.pk,
                user=self.user
            )
