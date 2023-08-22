from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from db.common.models import BaseModel, WithOwnerMixin
from db.common.types import UserModelType
from db.polls.models.constants import (
    QUESTION_TEXT_MAX_LEN,
    QUESTION_TEXT_MIN_LEN,
    QUESTION_TITLE_MAX_LEN,
    QUESTION_TITLE_MIN_LEN,
)

User: UserModelType = get_user_model()


title_validators = (
    MinLengthValidator(
        limit_value=QUESTION_TITLE_MIN_LEN,
        message="Question title must be at least %s characters long."
        % QUESTION_TITLE_MIN_LEN,
    ),
    MaxLengthValidator(
        limit_value=QUESTION_TITLE_MAX_LEN,
        message="Question title must be no longer than %s characters long."
        % QUESTION_TITLE_MAX_LEN,
    ),
)

text_validators = (
    MinLengthValidator(
        limit_value=QUESTION_TEXT_MIN_LEN,
        message="Question text must be at least %s characters long."
        % QUESTION_TEXT_MIN_LEN,
    ),
    MaxLengthValidator(
        limit_value=QUESTION_TEXT_MAX_LEN,
        message="Question text must be no longer than %s characters long."
        % QUESTION_TEXT_MAX_LEN,
    ),
)


class Question(
    WithOwnerMixin,
    BaseModel,
):
    title = models.CharField(
        max_length=QUESTION_TITLE_MAX_LEN,
        validators=title_validators,
    )
    text = models.CharField(
        max_length=QUESTION_TEXT_MAX_LEN,
        validators=text_validators,
    )

    def __str__(self):
        return self.title
