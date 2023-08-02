from typing import Any, Dict, List

import django_filters
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction

from db.common.types import UserModelType
from db.polls.models import Choice, Question, choice_set_validators
from services.common import model_update

__all__ = [
    "question_create",
    "question_destroy",
    "create_choice_instances",
    "create_question_instance",
    "question_update",
    "QuestionFilter",
]

User: UserModelType = get_user_model()


class QuestionFilter(django_filters.FilterSet):
    created_by__username = django_filters.CharFilter(
        field_name="created_by__username",
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
    *, question_pk: int, updated_by: UserModelType, data: Dict[str, Any]
) -> Question:
    question = Question.objects.get(pk=question_pk)
    if updated_by != question.created_by:
        raise PermissionDenied("You can't edit this question.")

    question, has_updated = model_update(
        instance=question, fields=["title", "text"], data=data
    )
    return question


def question_destroy(*, question_pk: int, destroyed_by: UserModelType):
    question = Question.objects.get(pk=question_pk)
    if destroyed_by != question.created_by:
        raise PermissionDenied("You can't delete this question.")
    question.delete()


def create_question_instance(
    *, title: str, text: str, created_by: UserModelType
) -> Question:
    question = Question(title=title, text=text, created_by=created_by)
    question.full_clean()
    return question


def create_choice_instances(*, choices: List[str], question: Question) -> List[Choice]:
    for validator in choice_set_validators:
        validator(choices)

    instances = [Choice(text=text, question=question) for text in choices]
    for instance in instances:
        instance.full_clean(validate_unique=False, validate_constraints=False)
    return instances


def question_create(
    *, title: str, text: str, created_by: UserModelType, choices: List[str]
) -> Question:
    question = create_question_instance(title=title, text=text, created_by=created_by)
    with transaction.atomic():
        question.save()
        choice_instances = create_choice_instances(choices=choices, question=question)
        Choice.objects.bulk_create(objs=choice_instances)
    return Question.objects.get(question_pk=question.pk, fetch_choices=True)
