from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from modules.document.application.use_cases.create_document import CreateDocumentUseCase
from modules.document.application.dtos import CreateDocumentDTO
from modules.document.infrastructure.repositories.document_repository_django import DjangoDocumentRepository
from .serializers import DocumentCreateSerializer, DocumentSerializer


class DocumentViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    def get_serializer_class(self):
        mapping = {
            'create': DocumentCreateSerializer,
        }
        return mapping.get(self.action, DocumentSerializer)

    @extend_schema(tags=["Document"], request=DocumentCreateSerializer, responses={201: DocumentSerializer})
    def create(self, request, *args, **kwargs):
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = CreateDocumentUseCase(DjangoDocumentRepository()).execute(CreateDocumentDTO(**data))
        return Response(DocumentSerializer(result).data, status=status.HTTP_201_CREATED)


