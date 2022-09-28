from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_title = models.CharField(max_length=40)
    question_text = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published',
                                    default=timezone.now,
                                    editable=False)

    def __str__(self):
        return self.question_text
