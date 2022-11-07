from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class QuestionConfig:
    TITLE_MIN_LEN = 40
    TITLE_MAX_LEN = 40
    TEXT_MIN_LEN = 20
    TEXT_MAX_LEN = 200
    CHOICES_MIN_NUMBER = 2
    CHOICES_MAX_NUMBER = 10


class Question(models.Model):
    question_title = models.CharField(
        max_length=QuestionConfig.TITLE_MAX_LEN,
        validators=[
            MinLengthValidator(
                limit_value=QuestionConfig.TITLE_MIN_LEN,
                message='Question title must be at least %s characters long.'
                        % QuestionConfig.TITLE_MIN_LEN
            ),
            MaxLengthValidator(
                limit_value=QuestionConfig.TITLE_MAX_LEN,
                message='Question title must less than %s characters long.'
                        % QuestionConfig.TITLE_MAX_LEN
            ),
        ]
    )
    question_text = models.CharField(
        max_length=QuestionConfig.TEXT_MAX_LEN,
        validators=[
            MinLengthValidator(
                limit_value=QuestionConfig.TEXT_MIN_LEN,
                message='Question text must be at least %s characters long.'
                        % QuestionConfig.TEXT_MIN_LEN
            ),
            MaxLengthValidator(
                limit_value=QuestionConfig.TEXT_MAX_LEN,
                message='Question title must less than %s characters long.'
                        % QuestionConfig.TEXT_MAX_LEN
            ),
        ]
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    pub_date = models.DateTimeField(
        'date published',
        default=timezone.now,
        editable=False
    )

    def __str__(self):
        return self.question_text

    def choices(self):
        return self.choice_set.all()
