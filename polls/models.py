from django.db import models
from uuid import uuid4


class Question(models.Model):
    question_title = models.CharField(max_length=40)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',
                                    auto_now=True,
                                    editable=False)
    question_slug = models.SlugField(max_length=60,
                                     unique=True,
                                     db_index=True,
                                     verbose_name="URL")

    def __str__(self):
        return self.question_text

    def choices(self):
        if not hasattr(self, "_choices"):
            self._choices = self.choice_set.all()
        return self._choices


class Choice(models.Model):
    choice_uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    choice_text = models.CharField(max_length=60)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('choice_text', 'question')

    def __str__(self):
        return self.choice_text

    def question_slug(self):
        return self.question.question_slug
