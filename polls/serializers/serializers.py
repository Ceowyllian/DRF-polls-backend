from django.db import transaction
from rest_framework.serializers import (
    ValidationError,
    ModelSerializer,
)

from polls import services
from polls.models import (
    Question,
    Choice,
    Vote,
)


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ['voted_by', 'date_voted', 'question']

    def create(self, validated_data):
        vote = services.vote.perform_vote(**validated_data)
        return vote


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text']


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_title', 'created_by', 'pub_date']
        read_only_fields = ['created_by', 'pub_date']

    def create(self, validated_data):
        raise NotImplementedError(
            "You must implement the creation of questions with multiple choices!"
        )


class QuestionWithChoicesSerializer(QuestionSerializer):
    choices = ChoiceSerializer(many=True, required=True)

    class Meta(QuestionSerializer.Meta):
        fields = '__all__'

    def validate_choices(self, choices_data):
        choices = [choice['choice_text'] for choice in choices_data]
        if len(choices) < 2:
            raise ValidationError('At least 2 choices are required.')
        if len(choices) > len(set(choices)):
            raise ValidationError('The answers to the question must be different.')
        return choices_data

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', None)
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)
        return question
