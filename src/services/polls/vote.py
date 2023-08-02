from django.core.exceptions import ValidationError

from db.common.types import UserModelType
from db.polls.models import Choice, Vote

__all__ = [
    "perform_vote",
    "cancel_vote",
]


def perform_vote(*, choice_pk: int, user: UserModelType):
    choice = Choice.objects.select_related("question").get(id=choice_pk)

    vote = Vote(choice=choice, question=choice.question, owner=user)
    vote.full_clean()
    vote.save()


def cancel_vote(*, choice_pk: int, user: UserModelType):
    choice = Choice.objects.get(id=choice_pk)

    number_deleted, _ = Vote.objects.filter(choice=choice, owner=user).delete()
    if number_deleted == 0:
        raise ValidationError("You didn't vote for this choice.")
