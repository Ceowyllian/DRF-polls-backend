from django.db import (
    models,
)
from django.db.models import UniqueConstraint

from . import Question


class Choice(models.Model):
    choice_text = models.CharField(max_length=60)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(name='no identical choices for question',
                             fields=['choice_text', 'question']),
        ]

    def __str__(self):
        return self.choice_text
