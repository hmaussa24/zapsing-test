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


class CompanyRegisterRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)


class CompanyRegisterResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()


class CompanyLoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CompanyLoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class CompanyMeResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()


