from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample

from modules.company.infrastructure.django_app.models import Company
from .token import encode, decode
from .serializers import (
    CompanyRegisterRequestSerializer,
    CompanyRegisterResponseSerializer,
    CompanyLoginRequestSerializer,
    CompanyLoginResponseSerializer,
    CompanyMeResponseSerializer,
)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@extend_schema(
    tags=["Company Auth"],
    request=CompanyRegisterRequestSerializer,
    responses={
        201: CompanyRegisterResponseSerializer,
        400: None,
    },
    examples=[
        OpenApiExample(
            'Registro ejemplo',
            value={"name": "Acme Corp", "email": "admin@acme.com", "password": "SecurePassword123"},
            request_only=True,
        ),
        OpenApiExample(
            'Respuesta registro',
            value={"id": 1, "name": "Acme Corp", "email": "admin@acme.com"},
            response_only=True,
        ),
    ],
)
def register(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    try:
        body = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'detail': 'Invalid JSON'}, status=400)
    name = (body.get('name') or '').strip()
    email = (body.get('email') or '').strip().lower()
    password = body.get('password') or ''
    if not name or not email or not password:
        return JsonResponse({'detail': 'Missing fields'}, status=400)
    if Company.objects.filter(email=email).exists():  # type: ignore[attr-defined]
        return JsonResponse({'detail': 'Email already registered'}, status=400)
    c = Company.objects.create(  # type: ignore[attr-defined]
        name=name,
        api_token='-',
        email=email,
        password_hash=make_password(password),
    )
    return JsonResponse({'id': c.id, 'name': c.name, 'email': c.email}, status=201)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@extend_schema(
    tags=["Company Auth"],
    request=CompanyLoginRequestSerializer,
    responses={
        200: CompanyLoginResponseSerializer,
        400: None,
    },
    examples=[
        OpenApiExample(
            'Login ejemplo',
            value={"email": "admin@acme.com", "password": "SecurePassword123"},
            request_only=True,
        ),
        OpenApiExample(
            'Respuesta login',
            value={"access": "<jwt>"},
            response_only=True,
        ),
    ],
)
def login(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    try:
        body = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'detail': 'Invalid JSON'}, status=400)
    email = (body.get('email') or '').strip().lower()
    password = body.get('password') or ''
    try:
        c = Company.objects.get(email=email)  # type: ignore[attr-defined]
    except Company.DoesNotExist:  # type: ignore[attr-defined]
        return JsonResponse({'detail': 'Invalid credentials'}, status=400)
    if not check_password(password, c.password_hash or ''):
        return JsonResponse({'detail': 'Invalid credentials'}, status=400)
    token = encode({'company_id': c.id, 'email': c.email})
    return JsonResponse({'access': token}, status=200)


@extend_schema(
    tags=["Company Auth"],
    responses={200: CompanyMeResponseSerializer, 401: None},
)
def me(request: HttpRequest):
    auth = request.META.get('HTTP_AUTHORIZATION') or ''
    if not auth.startswith('Bearer '):
        return JsonResponse({'detail': 'Unauthorized'}, status=401)
    token = auth[len('Bearer '):]
    payload = decode(token)
    if not payload or not payload.get('company_id'):
        return JsonResponse({'detail': 'Unauthorized'}, status=401)
    try:
        c = Company.objects.get(id=payload['company_id'])  # type: ignore[attr-defined]
    except Company.DoesNotExist:  # type: ignore[attr-defined]
        return JsonResponse({'detail': 'Unauthorized'}, status=401)
    return JsonResponse({'id': c.id, 'name': c.name, 'email': c.email}, status=200)


