from rest_framework import serializers


class ImageDimension(serializers.DictField):
    width = serializers.IntegerField(required=True)
    height = serializers.IntegerField(required=True)


class ImagePayload(serializers.DictField):
    data = serializers.CharField(required=True)
    dimensions = ImageDimension(required=True)


class ImageSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    payload = ImagePayload(required=True)
