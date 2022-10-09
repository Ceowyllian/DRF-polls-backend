from django.urls import path
from rest_framework.routers import DefaultRouter

from .apiviews import (
    QuestionViewSet,
    VoteView,
    UserCreate,
    LoginView,
)

router = DefaultRouter()
router.register('question', QuestionViewSet, basename='question')

urlpatterns = [
    path('votes/', VoteView.as_view(), name='vote'),
    path('users/', UserCreate.as_view(), name='user-create'),
    path('login/', LoginView.as_view(), name='login')
]

urlpatterns += router.urls
