from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel
from apps.common.types import UserModelType

User: UserModelType = get_user_model()


class QuestionConfig:
    TITLE_MIN_LEN = 40
    TITLE_MAX_LEN = 40
    TEXT_MIN_LEN = 20
    TEXT_MAX_LEN = 200


title_validators = (
    MinLengthValidator(
        limit_value=QuestionConfig.TITLE_MIN_LEN,
        message="Question title must be at least %s characters long."
        % QuestionConfig.TITLE_MIN_LEN,
    ),
    MaxLengthValidator(
        limit_value=QuestionConfig.TITLE_MAX_LEN,
        message="Question title must be no longer than %s characters long."
        % QuestionConfig.TITLE_MAX_LEN,
    ),
)

text_validators = (
    MinLengthValidator(
        limit_value=QuestionConfig.TEXT_MIN_LEN,
        message="Question text must be at least %s characters long."
        % QuestionConfig.TEXT_MIN_LEN,
    ),
    MaxLengthValidator(
        limit_value=QuestionConfig.TEXT_MAX_LEN,
        message="Question text must be no longer than %s characters long."
        % QuestionConfig.TEXT_MAX_LEN,
    ),
)


class Question(BaseModel):
    title = models.CharField(
        max_length=QuestionConfig.TITLE_MAX_LEN,
        validators=title_validators,
    )
    text = models.CharField(
        max_length=QuestionConfig.TEXT_MAX_LEN,
        validators=text_validators,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        editable=False,
    )
    pub_date = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="date published",
    )

    def __str__(self):
        return self.title


class QuestionVector(BaseModel):
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        editable=True,
        related_name="search",
    )
    title_and_text = SearchVectorField()

    class Meta:
        indexes = [
            GinIndex(fields=["title_and_text"]),
        ]
