from rest_framework import serializers


class CompanyCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    api_token = serializers.CharField(max_length=255)


class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    api_token = serializers.CharField(max_length=255)


class CompanyUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    api_token = serializers.CharField(max_length=255, required=False)


