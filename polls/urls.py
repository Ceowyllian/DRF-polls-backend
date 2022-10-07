from django.urls import path
from rest_framework.routers import DefaultRouter

from .apiviews import (
    QuestionViewSet,
    CreateVote,
    UserCreate,
    LoginView,
)


router = DefaultRouter()
router.register('question', QuestionViewSet, basename='question')

urlpatterns = [
    path('questions/<int:pk>/choices/<int:choice_pk>/vote/', CreateVote.as_view(), name='vote-create'),
    path('users/', UserCreate.as_view(), name='user-create'),
    path('login/', LoginView.as_view(), name='login')
]

urlpatterns += router.urls
