from django.db import models
from django.db.models import UniqueConstraint

from db.common.models import BaseModel


class Choice(BaseModel):
    text = models.TextField(
        null=False,
        blank=False,
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
