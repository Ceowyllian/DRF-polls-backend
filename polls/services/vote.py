from django.contrib.auth import get_user_model
from django.db import IntegrityError
# TODO: replace 'rest_framework.exceptions' with 'django.core.exceptions'
from rest_framework.exceptions import ValidationError

from polls.models import Vote, Choice

User = get_user_model()


def perform_vote(choice_pk: int, voted_by: User) -> Vote:
    choice = Choice.objects.select_related('question').get(id=choice_pk)
    vote = Vote(choice=choice, question=choice.question, voted_by=voted_by)
    vote.full_clean(validate_constraints=False, validate_unique=False)
    try:
        vote.save()
    except IntegrityError:
        raise ValidationError("You can't vote twice for the same question!")
    return vote
