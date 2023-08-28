from django.urls import include, path
from rest_framework_nested.routers import NestedSimpleRouter, SimpleRouter

from api.polls.views import ChoiceViewSet, QuestionViewSet, VoteCreateDeleteAPI

questions_router = SimpleRouter()
questions_router.register(r"questions", QuestionViewSet)
choices_router = NestedSimpleRouter(questions_router, "questions", lookup="question")
choices_router.register(r"choices", ChoiceViewSet, "question-choices")

urlpatterns = [
    path(r"", include(questions_router.urls)),
    path(r"", include(choices_router.urls)),
    path(r"votes/<uuid:pk>/", VoteCreateDeleteAPI.as_view(), name="vote"),
]
