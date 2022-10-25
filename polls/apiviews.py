from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Question
from .serializers import (
    QuestionSerializer,
    QuestionWithChoicesSerializer,
    VoteSerializer,
)


class QuestionViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Question.objects.all()
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('choice_set')
        if username := self.request.query_params.get('username'):
            queryset = queryset.filter(created_by__username=username)
        return queryset

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ('list', 'update', 'partial_update', 'destroy'):
            return QuestionSerializer
        if self.action in ('create', 'retrieve'):
            return QuestionWithChoicesSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)

    def perform_destroy(self, instance):
        if self.request.user != instance.created_by:
            raise PermissionDenied('You can not delete this question.')
        instance.delete()

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.created_by:
            raise PermissionDenied('You can not edit this question.')
        serializer.save()


class VoteView(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def perform_create(self, serializer: VoteSerializer):
        user = self.request.user
        serializer.save(voted_by=user)
