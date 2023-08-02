from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, views, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.polls.serializers import (
    QuestionCreateSerializer,
    QuestionDetailSerializer,
    QuestionListSerializer,
    QuestionUpdateSerializer,
)
from db.polls.models import Choice, Question
from services.polls import (
    QuestionFilter,
    cancel_vote,
    perform_vote,
    question_create,
    question_destroy,
    question_update,
)

__all__ = [
    "QuestionViewSet",
    "VoteCreateDeleteAPI",
]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related("created_by").prefetch_related(
        "choice_set"
    )
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_class = QuestionFilter
    search_fields = [
        "title",
        "text",
        "created_by__username",
    ]
    ordering = "-created"
    ordering_fields = [
        "title",
        "text",
        "created_by__username",
        "created",
        "modified",
    ]

    def get_serializer_class(self):
        return {
            "retrieve": QuestionDetailSerializer,
            "list": QuestionListSerializer,
        }[self.action]

    def create(self, request, *args, **kwargs):
        input_ = QuestionCreateSerializer(data=request.data)
        input_.is_valid(raise_exception=True)
        question = question_create(created_by=request.user, **input_.validated_data)
        output = QuestionDetailSerializer(
            instance=question, context=self.get_serializer_context()
        )
        return Response(output.data, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        input_ = QuestionUpdateSerializer(data=request.data, partial=partial)
        input_.is_valid(raise_exception=True)
        question = question_update(
            question_pk=kwargs["pk"],
            updated_by=request.user,
            data=input_.validated_data,
        )
        output = QuestionDetailSerializer(
            instance=question, context=self.get_serializer_context()
        )
        return Response(output.data, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        question_destroy(question_pk=kwargs["pk"], destroyed_by=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def handle_exception(self, exc):
        if isinstance(exc, Question.DoesNotExist):
            raise Http404 from exc
        return super().handle_exception(exc)


class VoteCreateDeleteAPI(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        perform_vote(choice_pk=kwargs["pk"], user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        cancel_vote(choice_pk=kwargs["pk"], user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def handle_exception(self, exc):
        if isinstance(exc, Choice.DoesNotExist):
            raise Http404 from exc
        return super().handle_exception(exc)
