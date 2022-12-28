from typing import List, Dict, Any

import django_filters
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction, models

from common import UserModelType
from polls.models import (
    Question,
    Choice,
    choice_set_validators
)
from utils.services import model_update

User: UserModelType = get_user_model()


class QuestionFilter(django_filters.FilterSet):
    created_by = django_filters.CharFilter(
        field_name='created_by__username',
        lookup_expr='iexact'
    )
    title = django_filters.CharFilter(lookup_expr='icontains')
    text = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFromToRangeFilter(field_name='pub_date')

    class Meta:
        model = Question
        fields = ('title', 'text', 'created_by', 'pub_date')


def question_list(*, filters: Dict[str, Any] = None) -> models.QuerySet[Question]:
    filters = filters or {}
    qs = Question.objects.all()
    return QuestionFilter(filters, qs).qs


def retrieve(*, question_pk: int, fetch_choices: bool = False) -> Question:
    queryset = Question.objects.select_related('created_by')

    if fetch_choices:
        queryset = queryset.prefetch_related('choice_set')

    return queryset.get(id=question_pk)


def update(
        *,
        question_pk: int,
        updated_by: UserModelType,
        data: Dict[str, Any]
) -> Question:
    question = retrieve(question_pk=question_pk)
    if updated_by != question.created_by:
        raise PermissionDenied("You can't edit this question.")

    question, has_updated = model_update(
        instance=question,
        fields=['title', 'text'],
        data=data
    )
    return question


def destroy(*, question_pk: int, destroyed_by: UserModelType):
    question = retrieve(question_pk=question_pk)
    if destroyed_by != question.created_by:
        raise PermissionDenied("You can't delete this question.")
    question.delete()


def create_question_instance(
        *,
        title: str,
        text: str,
        created_by: UserModelType
) -> Question:
    question = Question(
        title=title,
        text=text,
        created_by=created_by
    )
    question.full_clean()
    return question


def create_choice_instances(
        *,
        choices: List[str],
        question: Question
) -> List[Choice]:
    for validator in choice_set_validators:
        validator.__call__(choices)

    instances = [Choice(text=text, question=question) for text in choices]
    for instance in instances:
        instance.full_clean(
            validate_unique=False, validate_constraints=False
        )
    return instances


def create(
        *,
        title: str,
        text: str,
        created_by: UserModelType,
        choices: List[str]
) -> Question:
    question = create_question_instance(
        title=title,
        text=text,
        created_by=created_by
    )
    with transaction.atomic():
        question.save()
        choice_instances = create_choice_instances(
            choices=choices, question=question
        )
        Choice.objects.bulk_create(objs=choice_instances)
    return retrieve(
        question_pk=question.pk, fetch_choices=True
    )
