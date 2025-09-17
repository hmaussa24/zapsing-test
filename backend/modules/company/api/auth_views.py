from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json

from modules.company.infrastructure.django_app.models import Company
from .token import encode, decode


@csrf_exempt
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


