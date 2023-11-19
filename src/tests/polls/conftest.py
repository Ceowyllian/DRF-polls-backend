from typing import Any

import pytest
from rest_framework.test import APIClient

from db.common.types import UserModelType
from db.polls.models import CHOICES_MAX_NUMBER, Choice, Question, Vote
from tests.polls.factories import (
    ChoiceFactory,
    QuestionChoicesDictFactory,
    QuestionDictFactory,
    QuestionFactory,
    VoteFactory,
)
from tests.users.factories import UserFactory


@pytest.fixture()
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture()
def question_dict() -> dict[str, Any]:
    return QuestionDictFactory()


@pytest.fixture()
def question_with_choices_dict():
    return QuestionChoicesDictFactory()


@pytest.fixture()
def invalid_question_dict():
    return {"title": "", "text": "", "choices": ["123"]}


@pytest.fixture()
def choice_list() -> list[str]:
    return [str(i) for i in range(CHOICES_MAX_NUMBER)]


@pytest.fixture()
def user(db) -> UserModelType:
    return UserFactory()


@pytest.fixture()
def another_user(db) -> UserModelType:
    return UserFactory()


@pytest.fixture()
def question(user) -> Question:
    """Question, created by fixture `user`."""
    return QuestionFactory(owner=user)


@pytest.fixture()
def choice_a(question) -> Choice:
    """Choice "A" related to fixture `question`."""
    return ChoiceFactory(text="A", question=question)


@pytest.fixture()
def choice_b(question) -> Choice:
    """Choice "B" related to fixture `question`."""
    return ChoiceFactory(text="B", question=question)


@pytest.fixture()
def vote(user, choice_a) -> Vote:
    """Fixture `user` voted for fixture `choice_a`"""
    return VoteFactory(
        owner=user,
        choice=choice_a,
        question=choice_a.question,
    )
