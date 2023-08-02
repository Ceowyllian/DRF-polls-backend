from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from db.common.models import BaseModel
from db.common.types import UserModelType

User: UserModelType = get_user_model()


class Vote(BaseModel):
    voted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date_voted = models.DateTimeField(auto_now=True, editable=False)
    question = models.ForeignKey(
        "polls.Question",
        on_delete=models.CASCADE,
        null=False,
    )
    choice = models.ForeignKey(
        "polls.Choice",
        on_delete=models.CASCADE,
        null=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="single_vote_for_question",
                fields=["question", "voted_by"],
                violation_error_message="You can only vote once per poll.",
            ),
        ]

    def clean(self):
        if self.question != self.choice.question:
            raise ValidationError("Choice is not related to question.")
