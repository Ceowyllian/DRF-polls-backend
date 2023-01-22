from rest_framework import serializers


class ModelSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    def save(self, **kwargs):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
