from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from modules.signer.application.use_cases.add_signer_to_document import AddSignerToDocumentUseCase
from modules.signer.application.dtos import CreateSignerDTO
from modules.signer.infrastructure.repositories.signer_repository_django import DjangoSignerRepository
from .serializers import SignerSerializer, SignerCreateSerializer


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
        document_id = int(request.query_params.get('document_id'))
        items = DjangoSignerRepository().list_by_document(document_id)
        return Response([SignerSerializer(i).data for i in items])

    @extend_schema(tags=["Signer"], request=SignerCreateSerializer, responses={201: SignerSerializer})
    def create(self, request, *args, **kwargs):
        serializer = SignerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = CreateSignerDTO(**serializer.validated_data)
        created = AddSignerToDocumentUseCase(DjangoSignerRepository()).execute(dto)
        return Response(SignerSerializer(created).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Signer"], responses={204: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        ok = DjangoSignerRepository().delete(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT if ok else status.HTTP_404_NOT_FOUND)


