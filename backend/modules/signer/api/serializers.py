from rest_framework import serializers
from modules.signer.application.dtos import SignerDTO, CreateSignerDTO


class SignerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    document_id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()


class SignerCreateSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()


