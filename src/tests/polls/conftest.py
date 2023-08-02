import pytest
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient

from db.common.types import UserModelType
from db.polls.models import Choice, ChoiceConfig, Question, QuestionConfig, Vote


@pytest.fixture()
def api_client() -> APIClient:
    client = APIClient()
    return client


@pytest.fixture()
def valid_question_dict():
    return {
        "title": "Test question 94452132-8a83-4521-b889abc",
        "text": "Test question text e2160d36-b68b-4b26-ad9d-a20f096166a4",
        "choices": ["a", "b", "c"],
    }


@pytest.fixture()
def invalid_question_dict():
    return {"title": "", "text": "", "choices": []}


@pytest.fixture()
def user(django_user_model: UserModelType) -> UserModelType:
    return django_user_model.objects.create_user(
        username="TestUserA", email="testmailA@mail.com", password="mRCk1XPhTPQEvakVzfF"
    )


@pytest.fixture()
def another_user(django_user_model: UserModelType) -> UserModelType:
    return django_user_model.objects.create_user(
        username="TestUserB", email="testmailB@mail.com", password="mRCk1XPhTPQEvakVzfF"
    )


@pytest.fixture()
def question(user) -> Question:
    """Question, created by fixture `user`."""

    return Question.objects.create(
        title="Test question", text="Test question text", created_by=user
    )


@pytest.fixture()
def choice_a(question):
    """Choice "A" related to fixture `question`."""
    return Choice.objects.create(text="A", question=question)


@pytest.fixture()
def choice_b(question):
    """Choice "B" related to fixture `question`."""
    return Choice.objects.create(text="B", question=question)


@pytest.fixture()
def vote(user, choice_a):
    """Fixture `user` voted for fixture `choice_a`"""
    return Vote.objects.create(
        choice=choice_a, question=choice_a.question, voted_by=user
    )


class Q:
    class title:
        @staticmethod
        def valid():
            return get_random_string(QuestionConfig.TITLE_MAX_LEN)

        @staticmethod
        def too_long():
            return get_random_string(QuestionConfig.TITLE_MAX_LEN + 1)

        @staticmethod
        def too_short():
            return get_random_string(QuestionConfig.TITLE_MIN_LEN - 1)

    class text:
        @staticmethod
        def valid():
            return get_random_string(QuestionConfig.TEXT_MAX_LEN)

        @staticmethod
        def too_long():
            return get_random_string(QuestionConfig.TEXT_MAX_LEN + 1)

        @staticmethod
        def too_short():
            return get_random_string(QuestionConfig.TEXT_MIN_LEN - 1)


class C:
    class number:
        @staticmethod
        def valid():
            return ChoiceConfig.CHOICES_MAX_NUMBER

        @staticmethod
        def too_many():
            return ChoiceConfig.CHOICES_MAX_NUMBER + 1

        @staticmethod
        def too_few():
            return ChoiceConfig.CHOICES_MIN_NUMBER - 1

    class text:
        @staticmethod
        def valid():
            i = 0
            while True:
                i += 1
                yield get_random_string(ChoiceConfig.TEXT_MAX_LEN - len(str(i))) + str(
                    i
                )

        @staticmethod
        def empty():
            while True:
                yield ""

        @staticmethod
        def too_long():
            i = 0
            while True:
                i += 1
                yield get_random_string(ChoiceConfig.TEXT_MAX_LEN) + str(i)

        @staticmethod
        def identical():
            text = get_random_string(ChoiceConfig.TEXT_MAX_LEN)
            while True:
                yield text
