from django.urls import path

from .apiviews import (
    QuestionListCreateAPI,
    QuestionRetrieveUpdateDeleteAPI,
    VoteCreateAPI,
)

urlpatterns = [
    path('questions/', QuestionListCreateAPI.as_view()),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDeleteAPI.as_view()),
    path('votes/', VoteCreateAPI.as_view(), name='vote'),
]
