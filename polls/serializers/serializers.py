from rest_framework.serializers import (
    ModelSerializer,
)

from polls.models import (
    Question,
    Choice,
    Vote,
)
from polls.services.question import create_question_with_choices
from polls.services.vote import perform_vote


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ['choice']

    def create(self, validated_data):
        vote = perform_vote(**validated_data)
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

    default_error_messages = {
        'too few choices': 'At least 2 choices are required.',
        'identical choices': 'The answers to the question must be different.',
    }

    class Meta(QuestionSerializer.Meta):
        fields = '__all__'

    def validate_choices(self, choices_data):
        choices = [choice['choice_text'] for choice in choices_data]
        if len(choices) < 2:
            self.fail('too few choices')
        if len(choices) > len(set(choices)):
            self.fail('identical choices')
        return choices_data

    def create(self, validated_data):
        question = create_question_with_choices(**validated_data)
        return question
