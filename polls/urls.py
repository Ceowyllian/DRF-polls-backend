from django.urls import path
from rest_framework.routers import DefaultRouter

from .apiviews import (
    QuestionViewSet,
    VoteView,
)

router = DefaultRouter()
router.register('question', QuestionViewSet, basename='question')

urlpatterns = [
    path('votes/', VoteView.as_view(), name='vote'),
]

urlpatterns += router.urls
