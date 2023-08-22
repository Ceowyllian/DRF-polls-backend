from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.db.models import UniqueConstraint

from db.common.models import BaseModel
from db.polls.models.constants import CHOICE_TEXT_MAX_LEN, CHOICE_TEXT_MIN_LEN

text_validators = (
    MinLengthValidator(
        limit_value=CHOICE_TEXT_MIN_LEN,
        message="Choice text must be at least %s characters long."
        % (CHOICE_TEXT_MIN_LEN - 1),
    ),
    MaxLengthValidator(
        limit_value=CHOICE_TEXT_MAX_LEN,
        message="Choice title must be no longer than %s characters long."
        % CHOICE_TEXT_MAX_LEN,
    ),
)


class Choice(BaseModel):
    text = models.CharField(
        max_length=CHOICE_TEXT_MAX_LEN,
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
