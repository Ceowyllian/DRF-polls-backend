from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from polls.models import Question


@receiver(pre_save, sender=Question)
def set_question_slug(sender, instance: Question, raw, using, update_fields, **kwargs):
    slug = slugify(instance.question_title)
    if not instance.question_slug.startswith(slug):
        while True:
            try:
                Question.objects.get(question_slug=slug)
            except Question.DoesNotExist:
                instance.question_slug = slug
                return
            else:
                slug += '-'
