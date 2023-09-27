from typing import Any, Dict, Sequence

import django_filters
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction

from db.common.types import UserModelType
from db.polls.models import Question
from services.common import model_update
from services.polls.choice import choices_create

__all__ = [
    "question_create",
    "question_destroy",
    "question_update",
    "QuestionFilter",
]

User: UserModelType = get_user_model()


class QuestionFilter(django_filters.FilterSet):
    owner__username = django_filters.CharFilter(
        field_name="owner__username",
        lookup_expr="iexact",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created",
        lookup_expr="lte",
    )
    created_after = django_filters.DateTimeFilter(
        field_name="created",
        lookup_expr="gte",
    )
    modified_before = django_filters.DateTimeFilter(
        field_name="modified",
        lookup_expr="lte",
    )
    modified_after = django_filters.DateTimeFilter(
        field_name="modigied",
        lookup_expr="gte",
    )


def question_update(
    *, question: Question, updated_by: UserModelType, data: Dict[str, Any]
) -> Question:
    if updated_by != question.owner:
        raise PermissionDenied("You can't edit this question.")

    question, has_updated = model_update(
        instance=question, fields=["title", "text"], data=data
    )
    return question


def question_destroy(*, question: Question, destroyed_by: UserModelType):
    if destroyed_by != question.owner:
        raise PermissionDenied("You can't delete this question.")
    question.delete()


def question_create(
    *, title: str, text: str, created_by: UserModelType, choices: Sequence[str]
) -> Question:
    question = Question(title=title, text=text, owner=created_by)
    question.full_clean()
    with transaction.atomic():
        question.save()
        choices_create(new_choices=choices, question=question)
    return Question.objects.get(id=question.pk)
