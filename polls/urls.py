from django.urls import path

from .apiviews import (
    QuestionListCreateAPI,
    QuestionRetrieveUpdateDeleteAPI,
    VoteCreateDeleteAPI,
)

urlpatterns = [
    path('questions/', QuestionListCreateAPI.as_view()),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDeleteAPI.as_view(), name='question-detail'),
    path('votes/<int:pk>/', VoteCreateDeleteAPI.as_view(), name='vote'),
]
