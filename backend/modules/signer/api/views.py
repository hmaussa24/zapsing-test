from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from modules.signer.application.use_cases.add_signer_to_document import AddSignerToDocumentUseCase
from modules.signer.application.dtos import CreateSignerDTO
from modules.signer.infrastructure.repositories.signer_repository_django import DjangoSignerRepository
from .serializers import SignerSerializer, SignerCreateSerializer
from modules.company.api.token import company_id_from_request
from modules.document.infrastructure.repositories.document_repository_django import DjangoDocumentRepository


class SignerViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    def get_serializer_class(self):
        return {
            'list': SignerSerializer,
            'create': SignerCreateSerializer,
        }.get(self.action, SignerSerializer)

    @extend_schema(tags=["Signer"], responses=SignerSerializer(many=True))
    def list(self, request, *args, **kwargs):
        cid = company_id_from_request(request)
        if not cid:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        document_id = int(request.query_params.get('document_id'))
        doc = DjangoDocumentRepository().get_by_id(document_id)
        if not doc or doc.company_id != cid:
            return Response([], status=status.HTTP_200_OK)
        items = DjangoSignerRepository().list_by_document(document_id)
        return Response([SignerSerializer(i).data for i in items])

    @extend_schema(tags=["Signer"], request=SignerCreateSerializer, responses={201: SignerSerializer})
    def create(self, request, *args, **kwargs):
        serializer = SignerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cid = company_id_from_request(request)
        if not cid:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        dto = CreateSignerDTO(**serializer.validated_data)
        doc = DjangoDocumentRepository().get_by_id(dto.document_id)
        if not doc or doc.company_id != cid:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        created = AddSignerToDocumentUseCase(DjangoSignerRepository()).execute(dto)
        return Response(SignerSerializer(created).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Signer"], responses={204: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        cid = company_id_from_request(request)
        if not cid:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        # Verify signer belongs to a document of this company
        try:
            signer_id = int(pk)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        repo = DjangoSignerRepository()
        # get signer via list/query; simplistic: try to infer via ORM
        from modules.signer.infrastructure.django_app.models import Signer as ORMSigner  # type: ignore
        try:
            s = ORMSigner.objects.select_related('document').get(id=signer_id)  # type: ignore[attr-defined]
        except ORMSigner.DoesNotExist:  # type: ignore[attr-defined]
            return Response(status=status.HTTP_404_NOT_FOUND)
        if getattr(s, 'document').company_id != cid:  # type: ignore[attr-defined]
            return Response(status=status.HTTP_404_NOT_FOUND)
        ok = repo.delete(signer_id)
        return Response(status=status.HTTP_204_NO_CONTENT if ok else status.HTTP_404_NOT_FOUND)


