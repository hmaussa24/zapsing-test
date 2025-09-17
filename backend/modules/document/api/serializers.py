from rest_framework import serializers


class DocumentCreateSerializer(serializers.Serializer):
    company_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    pdf_url = serializers.URLField(max_length=4096)


class DocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    company_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    pdf_url = serializers.URLField(max_length=4096)
    status = serializers.CharField()
    open_id = serializers.CharField(allow_null=True, required=False)
    token = serializers.CharField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    has_analysis = serializers.BooleanField(required=False)
    risk_score = serializers.FloatField(required=False)


class DocumentUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    pdf_url = serializers.URLField(required=False, max_length=4096)
    status = serializers.CharField(required=False)


