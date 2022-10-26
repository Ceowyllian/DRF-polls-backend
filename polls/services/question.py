from typing import List, TypedDict

from django.contrib.auth import get_user_model
from django.db import transaction

from polls.models import Question, Choice as ChoiceModel

User = get_user_model()


class Choice(TypedDict):
    choice_text: str


def create_question_with_choices(
        question_title: str,
        question_text: str,
        created_by: User,
        choices: List[Choice]
) -> Question:
    with transaction.atomic():
        question = Question.objects.create(
            question_title=question_title,
            question_text=question_text,
            created_by=created_by,
        )
        for choice_attrs in choices:
            ChoiceModel.objects.create(
                **choice_attrs,
                question=question
            )
    return question
