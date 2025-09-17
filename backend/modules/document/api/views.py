from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from modules.document.api.container import (
    make_create_document_use_case,
    make_list_documents_use_case,
    make_get_document_use_case,
    make_update_document_partial_use_case,
    make_delete_document_use_case,
)
from modules.document.application.use_cases.send_document_to_sign import SendDocumentToSignUseCase
from modules.document.application.ports import DocumentCommandRepository, DocumentQueryRepository
from modules.company.infrastructure.repositories.company_repository_django import DjangoCompanyRepository
from modules.signer.infrastructure.repositories.signer_repository_django import DjangoSignerRepository
from modules.document.infrastructure.adapters.zapsign_client_http import HttpZapSignClient
from modules.document.application.dtos import CreateDocumentDTO
from modules.company.api.token import company_id_from_request
from modules.document.infrastructure.repositories.document_repository_django import DjangoDocumentRepository
from modules.company.infrastructure.repositories.company_repository_django import DjangoCompanyRepository
from modules.document.infrastructure.adapters.zapsign_client_http import HttpZapSignClient
from .serializers import DocumentCreateSerializer, DocumentSerializer, DocumentUpdateSerializer
from modules.analysis.infrastructure.repositories.analysis_repository_django import DjangoAnalysisRepository


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
        cid = company_id_from_request(request)
        if not cid:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        result = make_create_document_use_case().execute(CreateDocumentDTO(company_id=cid, name=data['name'], pdf_url=data['pdf_url']))
        return Response(DocumentSerializer(result).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Document"], responses=DocumentSerializer(many=True))
    def list(self, request, *args, **kwargs):
        company_id = company_id_from_request(request)
        if not company_id:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        page_dto = make_list_documents_use_case().execute(company_id=company_id, page=page, page_size=page_size)
        # Adaptador HTTP: devuelve estructura paginada
        return Response({
            'count': page_dto.count,
            'next': page_dto.next,
            'previous': page_dto.previous,
            'results': [DocumentSerializer(i).data for i in page_dto.results]
        })

    @extend_schema(tags=["Document"], responses=DocumentSerializer)
    def retrieve(self, request, pk=None, *args, **kwargs):
        item = make_get_document_use_case().execute(int(pk))
        if not item:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        cid = company_id_from_request(request)
        if not cid or item.company_id != cid:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(DocumentSerializer(item).data)

    @extend_schema(tags=["Document"], request=DocumentUpdateSerializer, responses=DocumentSerializer)
    def partial_update(self, request, pk=None, *args, **kwargs):
        serializer = DocumentUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        current = make_get_document_use_case().execute(int(pk))
        cid = company_id_from_request(request)
        if not current or not cid or current.company_id != cid:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        updated = make_update_document_partial_use_case().execute(int(pk), **serializer.validated_data)
        if not updated:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(DocumentSerializer(updated).data)

    @extend_schema(tags=["Document"], responses={204: None, 404: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        current = make_get_document_use_case().execute(int(pk))
        cid = company_id_from_request(request)
        if not current or not cid or current.company_id != cid:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ok = make_delete_document_use_case().execute(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT if ok else status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='send_to_sign')
    @extend_schema(tags=["Document"], responses=DocumentSerializer)
    def send_to_sign(self, request, pk=None, *args, **kwargs):
        doc_commands: DocumentCommandRepository = DjangoDocumentRepository()
        doc_queries: DocumentQueryRepository = DjangoDocumentRepository()
        use_case = SendDocumentToSignUseCase(
            document_commands=doc_commands,
            document_queries=doc_queries,
            company_queries=DjangoCompanyRepository(),
            signer_queries=DjangoSignerRepository(),
            zap_sign_client=HttpZapSignClient(),
        )
        result = use_case.execute(int(pk))
        if not result:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(DocumentSerializer(result).data)

    @action(detail=True, methods=['get'], url_path='analysis')
    @extend_schema(tags=["Document"], responses={200: None, 404: None})
    def analysis(self, request, pk=None, *args, **kwargs):
        repo = DjangoAnalysisRepository()
        dto = repo.get_by_document_id(int(pk))
        if not dto:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'document_id': dto.document_id,
            'summary': dto.summary,
            'labels': dto.labels,
            'entities': dto.entities,
            'risk_score': dto.risk_score,
            'status': dto.status,
        })

