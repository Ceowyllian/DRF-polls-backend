from typing import List, Dict, Any

from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction

from polls.models import (
    Question,
    Choice,
    QuestionConfig
)
from utils.services import model_update


def retrieve(question_pk: int, prefetch_choices: object = False) -> Question:
    queryset = Question.objects.select_related('created_by')
    if prefetch_choices:
        queryset = queryset.prefetch_related('choice_set')
    return queryset.get(id=question_pk)


def update(question_pk: int, updated_by: Any, data: Dict[str, Any]) -> Question:
    question = retrieve(question_pk=question_pk)
    if updated_by != question.created_by:
        raise PermissionDenied("You can't edit this question.")

    question, has_updated = model_update(
        instance=question,
        fields=['title', 'text'],
        data=data
    )
    return question


def destroy(question_pk: int, destroyed_by: Any):
    question = retrieve(question_pk=question_pk)
    if destroyed_by != question.created_by:
        raise PermissionDenied("You can't delete this question.")
    question.delete()


def create_question_instance(title: str, text: str, created_by: Any) -> Question:
    question = Question(
        title=title,
        text=text,
        created_by=created_by
    )
    question.full_clean()
    return question


def create_choice_instances(choices: List[str], question: Question) -> List[Choice]:
    number = len(choices)
    if number > QuestionConfig.CHOICES_MAX_NUMBER:
        raise ValidationError(
            'Too many choices, maximum %s allowed.'
            % QuestionConfig.CHOICES_MAX_NUMBER
        )
    if number < QuestionConfig.CHOICES_MIN_NUMBER:
        raise ValidationError(
            'Too few choices, minimum %s required.'
            % QuestionConfig.CHOICES_MIN_NUMBER
        )
    if number > len(set(choices)):
        raise ValidationError('The choices must be different.')
    instances = [Choice(text=text, question=question) for text in choices]
    for instance in instances:
        instance.full_clean(validate_unique=False, validate_constraints=False)
    return instances


def create(title: str, text: str, created_by: Any, choices: List[str]) -> Question:
    question = create_question_instance(title, text, created_by)
    with transaction.atomic():
        question.save()
        choice_instances = create_choice_instances(choices=choices, question=question)
        Choice.objects.bulk_create(objs=choice_instances)
    return retrieve(question_pk=question.pk, prefetch_choices=True)
