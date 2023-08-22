from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.db.models import UniqueConstraint

from db.common.models import BaseModel


class ChoiceConfig:
    TEXT_MIN_LEN = 1
    TEXT_MAX_LEN = 60
    CHOICES_MIN_NUMBER = 2
    CHOICES_MAX_NUMBER = 10


text_validators = (
    MinLengthValidator(
        limit_value=ChoiceConfig.TEXT_MIN_LEN,
        message="Choice text must be at least %s characters long."
        % (ChoiceConfig.TEXT_MIN_LEN - 1),
    ),
    MaxLengthValidator(
        limit_value=ChoiceConfig.TEXT_MAX_LEN,
        message="Choice title must be no longer than %s characters long."
        % ChoiceConfig.TEXT_MAX_LEN,
    ),
)


class Choice(BaseModel):
    text = models.CharField(
        max_length=ChoiceConfig.TEXT_MAX_LEN,
        validators=text_validators,
    )
    question = models.ForeignKey(
        "polls.Question",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                name="no identical choices for question",
                fields=("text", "question"),
            ),
        )

    def __str__(self):
        return self.text
