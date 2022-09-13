from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Question, Choice
from .serializers import (
    QuestionListSerializer,
    QuestionSerializer,
    ChoiceSerializer,
)


@csrf_exempt
@api_view(['GET', 'POST'])
def questions(request):
    if request.method == 'GET':
        question_list = Question.objects.all()
        serializer = QuestionListSerializer(question_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionListSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.create(serializer.validated_data)
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
def question_detail(request, question_slug: str):
    question = get_object_or_404(Question, question_slug=question_slug)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        question.delete()
        return Response('Question deleted', status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
def choices(request, question_slug: str):
    question = get_object_or_404(Question, question_slug=question_slug)

    if request.method == 'GET':
        serializer = ChoiceSerializer(question.choices(), many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ChoiceSerializer(data={
            'question_id': question.id,
            **request.data,
        })
        if serializer.is_valid():
            choice = serializer.save()
            return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
def choice_detail(request, question_slug: str, choice_uuid: str):
    choice = get_object_or_404(Choice,
                               question__question_slug=question_slug,
                               choice_uuid=choice_uuid)

    if request.method == 'GET':
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = ChoiceSerializer(choice, data=request.data, partial=True)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(ChoiceSerializer(choice).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        choice.delete()
        return Response('Choice deleted', status=status.HTTP_204_NO_CONTENT)
