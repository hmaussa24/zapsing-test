from django.http import HttpRequest
from django.contrib.auth.hashers import make_password, check_password
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

from modules.company.infrastructure.django_app.models import Company
from .token import company_id_from_request
from .serializers import (
    CompanyRegisterRequestSerializer,
    CompanyRegisterResponseSerializer,
    CompanyLoginRequestSerializer,
    CompanyLoginResponseSerializer,
    CompanyMeResponseSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
@extend_schema(tags=["Company Auth"], request=CompanyRegisterRequestSerializer, responses={201: CompanyRegisterResponseSerializer, 400: None})
def register(request: HttpRequest):
    if request.method != 'POST':
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        body = json.loads(request.body.decode('utf-8'))
    except Exception:
        return Response({'detail': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    name = (body.get('name') or '').strip()
    email = (body.get('email') or '').strip().lower()
    password = body.get('password') or ''
    if not name or not email or not password:
        return Response({'detail': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)
    if Company.objects.filter(email=email).exists():  # type: ignore[attr-defined]
        return Response({'detail': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
    c = Company.objects.create(  # type: ignore[attr-defined]
        name=name,
        api_token='-',
        email=email,
        password_hash=make_password(password),
    )
    return Response({'id': c.id, 'name': c.name, 'email': c.email}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
@extend_schema(tags=["Company Auth"], request=CompanyLoginRequestSerializer, responses={200: CompanyLoginResponseSerializer, 400: None})
def login(request: HttpRequest):
    if request.method != 'POST':
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        body = json.loads(request.body.decode('utf-8'))
    except Exception:
        return Response({'detail': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    email = (body.get('email') or '').strip().lower()
    password = body.get('password') or ''
    try:
        c = Company.objects.get(email=email)  # type: ignore[attr-defined]
    except Company.DoesNotExist:  # type: ignore[attr-defined]
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    if not check_password(password, c.password_hash or ''):
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken()
    # Claims en refresh y access
    refresh['company_id'] = c.id
    refresh['email'] = c.email
    access = refresh.access_token
    access['company_id'] = c.id
    access['email'] = c.email
    return Response({'access': str(access), 'refresh': str(refresh)}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Company Auth"],
    responses={200: CompanyMeResponseSerializer, 401: None},
)
def me(request: HttpRequest):
    auth = request.META.get('HTTP_AUTHORIZATION') or ''
    if not auth.startswith('Bearer '):
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    cid = company_id_from_request(request)
    if not cid:
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        c = Company.objects.get(id=cid)  # type: ignore[attr-defined]
    except Company.DoesNotExist:  # type: ignore[attr-defined]
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'id': c.id, 'name': c.name, 'email': c.email}, status=status.HTTP_200_OK)


