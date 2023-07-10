from django.http import Http404
from rest_framework import permissions, status, views
from rest_framework.response import Response

from apps.api.pagination import CursorPagination, get_paginated_response
from apps.polls import serializers, services
from apps.polls.models import Choice, Question


class QuestionListCreateAPI(views.APIView):
    def get_permissions(self):
        method = self.request.method
        if method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get(self, request, *args, **kwargs):
        filters_serializer = serializers.QuestionFilterSerializer(
            data=request.query_params,
            partial=True,
        )
        filters_serializer.is_valid(raise_exception=True)
        questions = services.question.question_list(
            filters=filters_serializer.validated_data
        )
        return get_paginated_response(
            pagination_class=CursorPagination,
            serializer_class=serializers.QuestionListSerializer,
            queryset=questions,
            request=request,
            view=self,
        )

    def post(self, request, *args, **kwargs):
        input = serializers.QuestionCreateSerializer(data=request.data)
        input.is_valid(raise_exception=True)
        question = services.question.create(
            created_by=request.user, **input.validated_data
        )
        output = serializers.QuestionDetailSerializer(
            instance=question, context={"request": request}
        )
        return Response(data=output.data, status=status.HTTP_201_CREATED)


class QuestionRetrieveUpdateDeleteAPI(views.APIView):
    def get_permissions(self):
        method = self.request.method
        if method in ("PUT", "PATCH", "DELETE"):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get(self, request, *args, **kwargs):
        question = services.question.retrieve(
            question_pk=kwargs["pk"], fetch_choices=True
        )
        output = serializers.QuestionDetailSerializer(
            instance=question, context={"request": request}
        )
        return Response(data=output.data)

    def delete(self, request, *args, **kwargs):
        services.question.destroy(question_pk=kwargs["pk"], destroyed_by=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, partial=False):
        input = serializers.QuestionUpdateSerializer(
            data=self.request.data, partial=partial
        )
        input.is_valid(raise_exception=True)
        question = services.question.update(
            question_pk=self.kwargs["pk"],
            updated_by=self.request.user,
            data=input.validated_data,
        )
        output = serializers.QuestionDetailSerializer(
            instance=question, context={"request": self.request}
        )

        return Response(data=output.data)

    def patch(self, request, *args, **kwargs):
        return self.perform_update(partial=True)

    def put(self, request, *args, **kwargs):
        return self.perform_update(partial=False)

    def handle_exception(self, exc):
        if isinstance(exc, Question.DoesNotExist):
            raise Http404 from exc
        return super().handle_exception(exc)


class VoteCreateDeleteAPI(views.APIView):
    def get_permissions(self):
        method = self.request.method
        if method in ("POST", "DELETE"):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def post(self, request, *args, **kwargs):
        services.vote.perform_vote(choice_pk=kwargs["pk"], user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        services.vote.cancel_vote(choice_pk=kwargs["pk"], user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def handle_exception(self, exc):
        if isinstance(exc, Choice.DoesNotExist):
            raise Http404 from exc
        return super().handle_exception(exc)
