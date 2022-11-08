from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from . import serializers, services
from .models import Question
from utils import views


class QuestionListCreateAPI(views.APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        queryset = Question.objects.all()
        serializer = serializers.QuestionListSerializer(instance=queryset, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        input = serializers.QuestionCreateSerializer(data=request.data)
        input.is_valid(raise_exception=True)
        question = services.question.create(
            **input.validated_data,
            created_by=request.user
        )
        output = serializers.QuestionDetailSerializer(instance=question)
        return Response(data=output.data, status=status.HTTP_201_CREATED)


class QuestionRetrieveUpdateDeleteAPI(views.APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        question = services.question.retrieve(
            question_pk=kwargs['pk'],
            prefetch_choices=True,
        )
        output = serializers.QuestionDetailSerializer(instance=question)
        return Response(data=output.data)

    def delete(self, request, *args, **kwargs):
        services.question.destroy(
            question_pk=kwargs['pk'],
            destroyed_by=request.user
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, partial=False):
        input = serializers.QuestionUpdateSerializer(
            data=self.request.data,
            partial=partial
        )
        input.is_valid(raise_exception=True)
        question = services.question.update(
            question_pk=self.kwargs['pk'],
            updated_by=self.request.user,
            data=input.validated_data
        )
        output = serializers.QuestionDetailSerializer(instance=question)
        return Response(data=output.data)

    def patch(self, request, *args, **kwargs):
        return self.perform_update(partial=True)

    def put(self, request, *args, **kwargs):
        return self.perform_update(partial=False)

    def handle_exception(self, exc):
        if isinstance(exc, Question.DoesNotExist):
            raise Http404
        return super().handle_exception(exc)


class VoteCreateAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        input = serializers.VoteCreateSerializer(data=request.data)
        input.is_valid(raise_exception=True)
        vote = services.vote.perform_vote(
            **input.validated_data,
            voted_by=request.user
        )
        output = serializers.VoteOutputSerializer(instance=vote)
        return Response(data=output.data, status=status.HTTP_201_CREATED)
