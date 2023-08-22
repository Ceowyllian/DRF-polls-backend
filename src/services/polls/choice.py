from typing import Iterable, Sequence

from django.core.exceptions import ValidationError
from django.db import transaction

from db.polls.models import CHOICES_MAX_NUMBER, CHOICES_MIN_NUMBER, Choice, Question


def validate_choice_set(choices):
    if len(choices) > len(set(choices)):
        raise ValidationError("The choices must be different")
    if len(choices) < CHOICES_MIN_NUMBER:
        raise ValidationError(
            message="Too few choices, minimum %s required." % CHOICES_MIN_NUMBER
        )
    if len(choices) > CHOICES_MAX_NUMBER:
        raise ValidationError(
            message="Too many choices, maximum %s allowed." % CHOICES_MAX_NUMBER,
        )


def choices_create(
    *, new_choices: Sequence[str], question: Question
) -> Sequence[Choice]:
    existing_choices = {choice.text for choice in question.choice_set.all()}
    validate_choice_set(existing_choices | set(new_choices))
    instances = [Choice(text=text, question=question) for text in new_choices]
    for instance in instances:
        instance.full_clean()
    question.choice_set.add(*instances, bulk=False)
    return instances


def choices_replace(*, question: Question, choices: Sequence[str]) -> Iterable[Choice]:
    with transaction.atomic():
        question.choice_set.all().delete()
        return choices_create(new_choices=choices, question=question)


def choice_update(*, choice: Choice, text: str):
    question = choice.question
    existing_choices = {choice.text for choice in question.choice_set.all()}
    validate_choice_set((existing_choices - {choice.text}) | {text})
    choice.text = text
    choice.save(update_fields=["text"])
    return choice


def choice_delete(*, choice: Choice):
    existing_choices_count = choice.question.choice_set.count()
    if existing_choices_count - 1 < CHOICES_MIN_NUMBER:
        raise ValidationError(
            "You cannot delete this answer option, otherwise there will be too "
            "few of them."
        )
    choice.delete()
