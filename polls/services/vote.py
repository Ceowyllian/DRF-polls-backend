from django.contrib.auth import get_user_model

from polls.models import Vote, Choice

User = get_user_model()


def perform_vote(choice_pk: int, voted_by: User) -> Vote:
    choice = Choice.objects.select_related('question').get(id=choice_pk)
    vote = Vote(choice=choice, question=choice.question, voted_by=voted_by)

    vote.full_clean()
    vote.save()
    return vote
