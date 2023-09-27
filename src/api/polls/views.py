from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.common.schema_tags import SCHEMA_TAG_POLLS
from api.polls.serializers import (
    ChoiceDetailSerializer,
    ChoicesCreateSerializer,
    ChoiceUpdateSerializer,
    QuestionCreateSerializer,
    QuestionDetailSerializer,
    QuestionListSerializer,
    QuestionStatisticsSerializer,
    QuestionUpdateSerializer,
)
from db.polls.models import Choice, Question
from services.polls import (
    QuestionFilter,
    cancel_vote,
    choice_delete,
    choice_update,
    choices_create,
    choices_replace,
    perform_vote,
    question_create,
    question_destroy,
    question_update,
    votes_per_question,
)

__all__ = [
    "QuestionViewSet",
    "VoteCreateDeleteAPI",
    "ChoiceViewSet",
]


@extend_schema_view(
    list=extend_schema(
        summary="Paginated list of questions",
        responses={200: QuestionListSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Create a question",
        request=QuestionCreateSerializer,
        responses={201: QuestionDetailSerializer},
    ),
    retrieve=extend_schema(
        summary="Single question with choices",
        responses={200: QuestionDetailSerializer},
    ),
    update=extend_schema(
        summary="Update all fields of the question",
        request=QuestionUpdateSerializer,
        responses={200: QuestionDetailSerializer},
    ),
    partial_update=extend_schema(
        summary="Update some fields of the question",
        request=QuestionUpdateSerializer(partial=True),
        responses={200: QuestionDetailSerializer},
    ),
    destroy=extend_schema(
        summary="Delete the question",
        responses={204: None},
    ),
)
@extend_schema(tags=[SCHEMA_TAG_POLLS])
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related("owner").prefetch_related("choice_set")
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

    @extend_schema(
        summary="Replace question choices",
        request=ChoicesCreateSerializer,
        responses={201: ChoiceDetailSerializer(many=True)},
        operation_id="api_polls_questions_choices_replace",
    )
    @action(
        methods=["PUT"],
        detail=True,
        pagination_class=None,
    )
    def choices(self, request, *args, **kwargs):
        question = self.get_object()
        input_ = ChoicesCreateSerializer(data=request.data)
        input_.is_valid(raise_exception=True)
        choices = choices_replace(question=question, **input_.validated_data)
        output = ChoiceDetailSerializer(choices, many=True)
        return Response(output.data, status.HTTP_201_CREATED)

    @extend_schema(
        summary="Calculate votes per choice for the specified question",
        responses={200: QuestionStatisticsSerializer(many=True)},
    )
    @action(
        methods=["GET"],
        detail=True,
        pagination_class=None,
    )
    def statistics(self, request, *args, **kwargs):
        statistics = votes_per_question(question=self.get_object())
        output = QuestionStatisticsSerializer(statistics, many=True)
        return Response(output.data, status.HTTP_200_OK)


@extend_schema(tags=[SCHEMA_TAG_POLLS])
@extend_schema_view(
    create=extend_schema(
        summary="Add new choices to question",
        request=ChoicesCreateSerializer,
        responses={201: ChoiceDetailSerializer(many=True)},
    ),
    update=extend_schema(
        summary="Update choice text",
        request=ChoiceUpdateSerializer,
        responses={200: ChoiceDetailSerializer},
    ),
    partial_update=extend_schema(
        summary="Update choice text",
        request=ChoiceUpdateSerializer(partial=True),
        responses={200: ChoiceDetailSerializer},
    ),
    destroy=extend_schema(
        summary="Destroy question choice",
        responses={204: None},
    ),
    list=extend_schema(
        summary="List of question choices",
        responses={200: ChoiceDetailSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Single choice",
        responses={200: ChoiceDetailSerializer},
    ),
)
class ChoiceViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    pagination_class = None

    def get_queryset(self):
        return Choice.objects.filter(question_id=self.kwargs["question_pk"])

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return ChoiceDetailSerializer

    def create(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs["question_pk"])
        input_ = ChoicesCreateSerializer(data=request.data)
        input_.is_valid(raise_exception=True)
        choices = choices_create(question=question, **input_.validated_data)
        output = ChoiceDetailSerializer(choices, many=True)
        return Response(output.data, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        input_ = ChoiceUpdateSerializer(data=request.data, partial=partial)
        input_.is_valid(raise_exception=True)
        choice = choice_update(choice=self.get_object(), **input_.validated_data)
        output = ChoiceDetailSerializer(choice)
        return Response(output.data, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        choice_delete(choice=self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=[SCHEMA_TAG_POLLS])
class VoteCreateDeleteAPI(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="Perform vote", responses={201: None})
    def post(self, request, *args, **kwargs):
        perform_vote(choice_pk=kwargs["pk"], user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(summary="Cancel vote", responses={204: None})
    def delete(self, request, *args, **kwargs):
        cancel_vote(choice_pk=kwargs["pk"], user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def handle_exception(self, exc):
        if isinstance(exc, Choice.DoesNotExist):
            raise Http404 from exc
        return super().handle_exception(exc)
