from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

from modules.company.application.dtos import CreateCompanyDTO
from modules.company.api.container import (
    make_create_company_use_case,
    make_list_companies_use_case,
    make_get_company_use_case,
    make_update_company_partial_use_case,
    make_delete_company_use_case,
)
from .serializers import CompanyCreateSerializer, CompanySerializer, CompanyUpdateSerializer
from modules.company.api.token import company_id_from_request


class CompanyViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """ViewSet delgado: delega en casos de uso/repos, serializers por acción."""

    # Fuente de verdad de contratos: serializers por acción
    def get_serializer_class(self):
        mapping = {
            'list': CompanySerializer,
            'retrieve': CompanySerializer,
            'create': CompanyCreateSerializer,
            'partial_update': CompanyUpdateSerializer,
            'update': CompanyUpdateSerializer,
            'destroy': CompanySerializer,
        }
        return mapping.get(self.action, CompanySerializer)
    @extend_schema(tags=["Company"], responses=CompanySerializer(many=True), description="Lista todas las compañías")
    def list(self, request, *args, **kwargs):
        cid = company_id_from_request(request)
        if not cid:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        # Un listado completo no tiene sentido para company-auth; devolvemos solo la propia
        item = make_get_company_use_case().execute(cid)
        items = [item] if item else []
        data = [CompanySerializer(i).data for i in items]
        return Response(data)

    @extend_schema(tags=["Company"], responses=CompanySerializer, description="Obtiene detalle de una compañía")
    def retrieve(self, request, pk=None, *args, **kwargs):
        cid = company_id_from_request(request)
        if not cid:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        if int(pk) != cid:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        item = make_get_company_use_case().execute(int(pk))
        if not item:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(CompanySerializer(item).data)

    @extend_schema(tags=["Company"], request=CompanyCreateSerializer, responses={201: CompanySerializer})
    def create(self, request, *args, **kwargs):
        serializer = CompanyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = make_create_company_use_case().execute(CreateCompanyDTO(**data))

        return Response(CompanySerializer(result).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Company"], request=CompanyUpdateSerializer, responses=CompanySerializer)
    def partial_update(self, request, pk=None, *args, **kwargs):
        serializer = CompanyUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        cid = company_id_from_request(request)
        if not cid or int(pk) != cid:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        updated = make_update_company_partial_use_case().execute(int(pk), **serializer.validated_data)
        if not updated:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(CompanySerializer(updated).data)

    @extend_schema(tags=["Company"], responses={204: None, 404: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        cid = company_id_from_request(request)
        if not cid or int(pk) != cid:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ok = make_delete_company_use_case().execute(int(pk))
        status_code = status.HTTP_204_NO_CONTENT if ok else status.HTTP_404_NOT_FOUND
        return Response(status=status_code)


