from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.common.serializers import HyperlinkedModelSerializer
from db.common.types import UserModelType
from db.polls.models import Question

__all__ = [
    "ChoicesCreateSerializer",
    "QuestionFilterSerializer",
    "QuestionCreateSerializer",
    "QuestionUpdateSerializer",
    "QuestionDetailSerializer",
    "QuestionListSerializer",
    "QuestionStatisticsSerializer",
    "VoteCreateSerializer",
    "ChoiceDetailSerializer",
    "ChoiceUpdateSerializer",
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


class ChoiceDetailSerializer(serializers.Serializer):
    pk = serializers.UUIDField()
    text = serializers.CharField()


class QuestionStatisticsSerializer(serializers.Serializer):
    choice_pk = serializers.UUIDField(source="pk")
    votes = serializers.IntegerField(source="vote__count")


class QuestionDetailSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ("url", "pk", "title", "text", "owner", "choices")
        extra_kwargs = {
            "url": {"view_name": "question-detail", "lookup_field": "pk"},
            "owner": {"view_name": "user-detail", "lookup_field": "username"},
        }

    choices = ChoiceDetailSerializer(many=True, source="choice_set")


class QuestionListSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ("url", "pk", "title", "owner")
        extra_kwargs = {
            "url": {"view_name": "question-detail", "lookup_field": "pk"},
            "owner": {"view_name": "user-detail", "lookup_field": "username"},
        }


class ChoicesCreateSerializer(serializers.Serializer):
    choices = serializers.ListSerializer(
        required=True,
        allow_null=False,
        allow_empty=False,
        child=serializers.CharField(
            required=True,
            allow_null=False,
            allow_blank=False,
        ),
    )


class ChoiceUpdateSerializer(serializers.Serializer):
    text = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
