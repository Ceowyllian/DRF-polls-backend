from rest_framework import serializers

from polls.models import (
    Question,
    Choice,
    ChoiceConfig,
)


class ReadOnlyModelSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class QuestionDetailSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    class ChoiceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Choice
            fields = ['choice_text']

    choices = ChoiceSerializer(many=True, required=True)


class QuestionListSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Question
        exclude = ['question_text']


class QuestionCreateSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Question
        fields = ['question_title', 'question_text', 'choices']

    choices = serializers.ListSerializer(
        child=serializers.CharField(
            min_length=ChoiceConfig.TEXT_MIN_LEN,
            max_length=ChoiceConfig.TEXT_MAX_LEN
        ),
    )


class QuestionUpdateSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Question
        fields = ['question_title', 'question_text']


class VoteSerializer(serializers.Serializer):
    choice_pk = serializers.IntegerField(min_value=1, required=True)
