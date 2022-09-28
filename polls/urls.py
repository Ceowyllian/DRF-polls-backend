from django.urls import path
from rest_framework.routers import DefaultRouter

from .apiviews import (
    QuestionViewSet,
    ChoiceList,
    CreateVote,
    UserCreate,
    LoginView,
)


router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')

urlpatterns = [
    path('questions/<int:pk>/choices/', ChoiceList.as_view(), name='choice_list'),
    path('questions/<int:pk>/choices/<int:choice_pk>/vote/', CreateVote.as_view(), name='create_vote'),
    path('users/', UserCreate.as_view(), name='user_create'),
    path('login/', LoginView.as_view(), name='login')
]

urlpatterns += router.urls
