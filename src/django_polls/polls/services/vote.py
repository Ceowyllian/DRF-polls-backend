from django.core.exceptions import ValidationError

from django_polls.common import UserModelType
from django_polls.polls.models import Choice, Vote


def perform_vote(*, choice_pk: int, user: UserModelType):
    choice = Choice.objects.select_related("question").get(id=choice_pk)

    vote = Vote(choice=choice, question=choice.question, voted_by=user)
    vote.full_clean()
    vote.save()


def cancel_vote(*, choice_pk: int, user: UserModelType):
    choice = Choice.objects.get(id=choice_pk)

    number_deleted, _ = Vote.objects.filter(choice=choice, voted_by=user).delete()
    if number_deleted == 0:
        raise ValidationError("You didn't vote for this choice.")
