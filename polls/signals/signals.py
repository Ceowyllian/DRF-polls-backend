from django.db.models.signals import pre_save
from django.dispatch import receiver

from polls.models import Vote


@receiver(pre_save, sender=Vote)
def choice_is_related_to_question(sender, instance: Vote, raw, using, update_fields, **kwargs):
    if instance.question != instance.choice.question:
        raise ValueError
