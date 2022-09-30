from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question, Choice
from .serializers import (
    QuestionSerializer,
    QuestionWithChoicesSerializer,
    ChoiceSerializer,
    VoteSerializer,
    UserSerializer,
)


class QuestionViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Question.objects.prefetch_related('choice_set')
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

    def destroy(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        if not request.user == question.created_by:
            raise PermissionDenied('You can not delete this poll.')
        return super().destroy(request, *args, **kwargs)


class ChoiceList(generics.CreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(question_id=self.kwargs['pk'])
        return queryset

    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        if not request.user == question.created_by:
            raise PermissionDenied('You can not create choice for this question.')
        return super().post(request, *args, **kwargs)


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def post(self, request: Request, pk, choice_pk):
        serializer = VoteSerializer(data={
            'choice': choice_pk,
            'question': pk,
            'voted_by': request.user.pk,
        })
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Wrong Credentials'},
                            status=status.HTTP_400_BAD_REQUEST)
