from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError, ModelSerializer

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
        choice = validated_data['choice']
        vote, created = Vote.objects.get_or_create(
            **validated_data, question=choice.question)
        if not created:
            raise ValidationError("You can't vote twice for the same choice!")
        return vote


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text']


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['created_by']


class QuestionWithChoicesSerializer(QuestionSerializer):
    choices = ChoiceSerializer(many=True, required=True)

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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
