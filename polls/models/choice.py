from django.core.validators import MaxLengthValidator
from django.db import (
    models,
)
from django.db.models import UniqueConstraint


class ChoiceConfig:
    TEXT_MIN_LEN = 1
    TEXT_MAX_LEN = 60


class Choice(models.Model):
    text = models.CharField(
        max_length=ChoiceConfig.TEXT_MAX_LEN,
        validators=[
            MaxLengthValidator(
                limit_value=ChoiceConfig.TEXT_MAX_LEN,
                message='Choice text must less than %s characters long.'
                        % ChoiceConfig.TEXT_MAX_LEN
            )
        ]
    )

    from .question import Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(name='no identical choices for question',
                             fields=['text', 'question']),
        ]

    def __str__(self):
        return self.text
