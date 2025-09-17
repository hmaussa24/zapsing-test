from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from modules.document.application.use_cases.create_document import CreateDocumentUseCase
from modules.document.application.use_cases.list_documents import ListDocumentsUseCase
from modules.document.application.use_cases.get_document import GetDocumentUseCase
from modules.document.application.use_cases.update_document_partial import UpdateDocumentPartialUseCase
from modules.document.application.use_cases.delete_document import DeleteDocumentUseCase
from modules.document.application.dtos import CreateDocumentDTO
from modules.document.infrastructure.repositories.document_repository_django import DjangoDocumentRepository
from modules.company.infrastructure.repositories.company_repository_django import DjangoCompanyRepository
from modules.document.infrastructure.adapters.zapsign_client_http import HttpZapSignClient
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
        use_case = CreateDocumentUseCase(
            document_repository=DjangoDocumentRepository(),
            company_repository=DjangoCompanyRepository(),
            zap_sign_client=HttpZapSignClient(),
        )
        result = use_case.execute(CreateDocumentDTO(**data))
        return Response(DocumentSerializer(result).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Document"], responses=DocumentSerializer(many=True))
    def list(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        use_case = ListDocumentsUseCase(DjangoDocumentRepository())
        page_dto = use_case.execute(company_id=int(company_id) if company_id else None, page=page, page_size=page_size)
        # Adaptador HTTP: devuelve estructura paginada
        return Response({
            'count': page_dto.count,
            'next': page_dto.next,
            'previous': page_dto.previous,
            'results': [DocumentSerializer(i).data for i in page_dto.results]
        })

    @extend_schema(tags=["Document"], responses=DocumentSerializer)
    def retrieve(self, request, pk=None, *args, **kwargs):
        item = GetDocumentUseCase(DjangoDocumentRepository()).execute(int(pk))
        if not item:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(DocumentSerializer(item).data)

    @extend_schema(tags=["Document"], request=DocumentUpdateSerializer, responses=DocumentSerializer)
    def partial_update(self, request, pk=None, *args, **kwargs):
        serializer = DocumentUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = UpdateDocumentPartialUseCase(DjangoDocumentRepository()).execute(int(pk), **serializer.validated_data)
        if not updated:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(DocumentSerializer(updated).data)

    @extend_schema(tags=["Document"], responses={204: None, 404: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        ok = DeleteDocumentUseCase(DjangoDocumentRepository()).execute(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT if ok else status.HTTP_404_NOT_FOUND)


