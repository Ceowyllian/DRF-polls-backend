from django.contrib.auth.models import User
from django.db import models

from . import Choice
from . import Question


class Vote(models.Model):
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_voted = models.DateTimeField(auto_now=True, editable=False)

    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 null=False)
    choice = models.ForeignKey(Choice,
                               on_delete=models.CASCADE,
                               null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(name='single_vote_for_question',
                                    fields=['question', 'voted_by']),
        ]
