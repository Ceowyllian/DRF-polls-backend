from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.serializers import ValidationError

from polls.models import Vote

User = get_user_model()


def perform_vote(choice, voted_by) -> Vote:
    try:
        vote, created = Vote.objects.get_or_create(
            choice=choice,
            question=choice.question,
            voted_by=voted_by
        )
    except IntegrityError:
        raise ValidationError("You can't vote twice for the same question!")

    # Raise an error if the vote already exists
    if not created:
        raise ValidationError("You can't vote twice for the same choice!")

    return vote
