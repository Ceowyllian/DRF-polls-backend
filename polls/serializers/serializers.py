from rest_framework import serializers

from polls.models import Choice, Question


class QuestionListSerializer(serializers.Serializer):
    question_title = serializers.CharField(max_length=40, required=True)
    question_text = serializers.CharField(max_length=200, required=True)
    pub_date = serializers.DateTimeField(read_only=True)
    question_slug = serializers.SlugField(read_only=True)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ChoiceSerializer(serializers.Serializer):
    choice_uuid = serializers.UUIDField(read_only=True)
    choice_text = serializers.CharField(max_length=200, required=True)
    votes = serializers.IntegerField(required=False)
    question_id = serializers.IntegerField(write_only=True, required=True)

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

    def update(self, instance: Choice, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionSerializer(QuestionListSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)
