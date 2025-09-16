from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from modules.document.application.use_cases.create_document import CreateDocumentUseCase
from modules.document.application.dtos import CreateDocumentDTO
from modules.document.infrastructure.repositories.document_repository_django import DjangoDocumentRepository
from .serializers import DocumentCreateSerializer, DocumentSerializer, DocumentUpdateSerializer


class DocumentViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    def get_serializer_class(self):
        mapping = {
            'list': DocumentSerializer,
            'retrieve': DocumentSerializer,
            'create': DocumentCreateSerializer,
            'partial_update': DocumentUpdateSerializer,
            'update': DocumentUpdateSerializer,
        }
        return mapping.get(self.action, DocumentSerializer)

    @extend_schema(tags=["Document"], request=DocumentCreateSerializer, responses={201: DocumentSerializer})
    def create(self, request, *args, **kwargs):
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = CreateDocumentUseCase(DjangoDocumentRepository()).execute(CreateDocumentDTO(**data))
        return Response(DocumentSerializer(result).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Document"], responses=DocumentSerializer(many=True))
    def list(self, request, *args, **kwargs):
        items = DjangoDocumentRepository().list_all()
        data = [DocumentSerializer(i).data for i in items]
        return Response(data)

    @extend_schema(tags=["Document"], responses=DocumentSerializer)
    def retrieve(self, request, pk=None, *args, **kwargs):
        item = DjangoDocumentRepository().get_by_id(int(pk))
        if not item:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(DocumentSerializer(item).data)

    @extend_schema(tags=["Document"], request=DocumentUpdateSerializer, responses=DocumentSerializer)
    def partial_update(self, request, pk=None, *args, **kwargs):
        serializer = DocumentUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = DjangoDocumentRepository().update_partial(int(pk), **serializer.validated_data)
        if not updated:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(DocumentSerializer(updated).data)

    @extend_schema(tags=["Document"], responses={204: None, 404: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        ok = DjangoDocumentRepository().delete(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT if ok else status.HTTP_404_NOT_FOUND)


