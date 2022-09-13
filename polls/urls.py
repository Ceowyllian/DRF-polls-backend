from django.urls import path

from . import apiviews


urlpatterns = [
    path('questions/', apiviews.questions, name='questions'),
    path('questions/<slug:question_slug>/', apiviews.question_detail, name='question_detail'),
    path('questions/<slug:question_slug>/choices/', apiviews.choices, name='choices'),
    path('questions/<slug:question_slug>/choices/<uuid:choice_uuid>/', apiviews.choice_detail, name='choice_detail'),
]
