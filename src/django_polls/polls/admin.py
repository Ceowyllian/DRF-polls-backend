from django.contrib import admin

from django_polls.polls.models import Choice, Question, Vote

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Vote)
