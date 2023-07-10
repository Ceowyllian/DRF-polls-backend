from rest_framework import serializers


class ModelSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def create(self, validated_data):
        raise NotImplementedError  # pragma: no cover

    def update(self, instance, validated_data):
        raise NotImplementedError  # pragma: no cover


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    def save(self, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def create(self, validated_data):
        raise NotImplementedError  # pragma: no cover

    def update(self, instance, validated_data):
        raise NotImplementedError  # pragma: no cover
