from django.urls import path

from .apiviews import (
    QuestionListCreateAPI,
    QuestionRetrieveUpdateDeleteAPI,
    VoteView,
)

urlpatterns = [
    path('questions/', QuestionListCreateAPI.as_view()),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDeleteAPI.as_view()),
    path('votes/', VoteView.as_view(), name='vote'),
]
