from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.common.serializers import HyperlinkedModelSerializer
from db.common.types import UserModelType
from db.polls.models import Question

__all__ = [
    "QuestionFilterSerializer",
    "QuestionCreateSerializer",
    "QuestionUpdateSerializer",
    "QuestionDetailSerializer",
    "QuestionListSerializer",
    "VoteCreateSerializer",
]

User: UserModelType = get_user_model()


class QuestionFilterSerializer(serializers.Serializer):
    search_query = serializers.CharField(required=False)
    created_by = serializers.CharField(required=False)
    date_before = serializers.DateField(required=False)
    date_after = serializers.DateField(required=False)


class QuestionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    choices = serializers.ListSerializer(
        required=True,
        child=serializers.CharField(),
    )


class QuestionUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    text = serializers.CharField(required=True)


class VoteCreateSerializer(serializers.Serializer):
    choice_pk = serializers.IntegerField(min_value=1, required=True)


class QuestionDetailSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ("url", "pk", "title", "text", "created_by", "choices")
        extra_kwargs = {
            "url": {"view_name": "question-detail", "lookup_field": "pk"},
            "created_by": {"view_name": "user-detail", "lookup_field": "username"},
        }

    class ChoiceSerializer(serializers.Serializer):
        pk = serializers.IntegerField()
        text = serializers.CharField()

    choices = ChoiceSerializer(many=True, source="choice_set")


class QuestionListSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ("url", "pk", "title", "created_by")
        extra_kwargs = {
            "url": {"view_name": "question-detail", "lookup_field": "pk"},
            "created_by": {"view_name": "user-detail", "lookup_field": "username"},
        }
