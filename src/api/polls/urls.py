from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.polls.views import QuestionViewSet, VoteCreateDeleteAPI

questions_router = SimpleRouter()
questions_router.register(r"questions", QuestionViewSet)

urlpatterns = [
    path(r"", include(questions_router.urls)),
    path(r"votes/<uuid:pk>/", VoteCreateDeleteAPI.as_view(), name="vote"),
]
