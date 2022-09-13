from django.http import (
    JsonResponse,
    HttpRequest,
    HttpResponse,
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser

from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def questions(request: HttpRequest):
    if request.method == 'GET':
        question_list = Question.objects.all()
        serializer = QuestionSerializer(question_list,
                                        many=True,
                                        context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        fields = JSONParser().parse(request)
        serializer = QuestionSerializer(data=fields, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def question_detail(request: HttpRequest, question_slug: str):
    try:
        question = Question.objects.get(question_slug=question_slug)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = QuestionSerializer(question, context={'request': request})
        print(serializer.__repr__())
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        updated_fields = JSONParser().parse(request)
        serializer = QuestionSerializer(question,
                                        data=updated_fields,
                                        context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        question.delete()
        return HttpResponse(status=204)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def choices(request: HttpRequest, question_slug: str):
    try:
        question = Question.objects.get(question_slug=question_slug)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ChoiceSerializer(question.choice_set,
                                      many=True,
                                      context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ChoiceSerializer(data=data, context={'request': request})
        serializer.data['question_id'] = question.id
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def choice_detail(request: HttpRequest, question_slug: str, choice_uuid: str):
    try:
        Question.objects.get(question_slug=question_slug)
        choice = Choice.objects.get(choice_uuid=choice_uuid)
    except (Question.DoesNotExist, Choice.DoesNotExist):
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ChoiceSerializer(choice, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        updated_fields = JSONParser().parse(request)
        serializer = ChoiceSerializer(choice,
                                      data=updated_fields,
                                      context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        choice.delete()
        return HttpResponse(status=204)
