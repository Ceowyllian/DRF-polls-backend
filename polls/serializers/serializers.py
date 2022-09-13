from rest_framework import serializers

from polls.models import Choice, Question


class QuestionListSerializer(serializers.Serializer):
    question_title = serializers.CharField(max_length=40, required=True)
    question_text = serializers.CharField(max_length=200, required=True)
    pub_date = serializers.DateTimeField(required=True)
    question_slug = serializers.SlugField()

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ChoiceListSerializer(serializers.Serializer):
    choice_uuid = serializers.UUIDField(required=False)
    choice_text = serializers.CharField(max_length=200, required=True)
    votes = serializers.IntegerField(required=False)

    def create(self, validated_data):
        question_slug = validated_data['question_slug']
        question = Question.objects.get(question_slug=question_slug)
        return question.choice_set.create(
            question=question,
            choice_text=validated_data['choice_text']
        )

    def update(self, instance: Choice, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionSerializer(QuestionListSerializer):
    choices = ChoiceListSerializer(many=True, read_only=True, required=False)


class ChoiceSerializer(ChoiceListSerializer):
    question = QuestionListSerializer()
