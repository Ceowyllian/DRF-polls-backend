from typing import Any, Dict, List

import django_filters
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchQuery
from django.core.exceptions import PermissionDenied
from django.db import models, transaction

from apps.common.types import UserModelType
from apps.polls.models import Choice, Question, choice_set_validators
from services.common import model_update

__all__ = [
    "question_list",
    "question_create",
    "question_destroy",
    "create_choice_instances",
    "create_question_instance",
    "question_retrieve",
    "question_update",
]

User: UserModelType = get_user_model()


class QuestionFilter(django_filters.FilterSet):
    created_by = django_filters.CharFilter(
        field_name="created_by__username", lookup_expr="iexact"
    )
    date_before = django_filters.DateFilter(field_name="created", lookup_expr="lte")
    date_after = django_filters.DateFilter(field_name="created", lookup_expr="gte")

    class Meta:
        model = Question
        fields = ["created_by", "date_before", "date_after"]


def question_list(*, filters: Dict[str, Any] = None) -> models.QuerySet[Question]:
    filters = filters or {}
    query_string = filters.pop("search_query", None)
    questions = QuestionFilter(data=filters, queryset=Question.objects.all()).qs
    if query_string:
        questions = questions.select_related("search")
        return questions.filter(search__title_and_text=SearchQuery(query_string))
    return questions


def question_retrieve(*, question_pk: int, fetch_choices: bool = False) -> Question:
    queryset = Question.objects.select_related("created_by")

    if fetch_choices:
        queryset = queryset.prefetch_related("choice_set")

    return queryset.get(id=question_pk)


def question_update(
    *, question_pk: int, updated_by: UserModelType, data: Dict[str, Any]
) -> Question:
    question = question_retrieve(question_pk=question_pk)
    if updated_by != question.created_by:
        raise PermissionDenied("You can't edit this question.")

    question, has_updated = model_update(
        instance=question, fields=["title", "text"], data=data
    )
    return question


def question_destroy(*, question_pk: int, destroyed_by: UserModelType):
    question = question_retrieve(question_pk=question_pk)
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
    return question_retrieve(question_pk=question.pk, fetch_choices=True)
