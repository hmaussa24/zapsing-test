from rest_framework import serializers


class DocumentCreateSerializer(serializers.Serializer):
    company_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    pdf_url = serializers.URLField()


class DocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    company_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    pdf_url = serializers.URLField()
    status = serializers.CharField()
    open_id = serializers.CharField(allow_null=True, required=False)
    token = serializers.CharField(allow_null=True, required=False)


