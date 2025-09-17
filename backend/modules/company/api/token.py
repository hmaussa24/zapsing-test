import base64
import hmac
import json
import time
from hashlib import sha256
from typing import Any, Dict, Optional

from django.conf import settings


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def _b64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode('utf-8'))


def _sign(message: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode('utf-8'), message, sha256).digest()
    return _b64url_encode(sig)


def encode(payload: Dict[str, Any], expires_in_seconds: int = 3600) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    body = payload.copy()
    body.setdefault('iat', now)
    body.setdefault('exp', now + expires_in_seconds)
    secret = getattr(settings, 'AUTH_JWT_SECRET', None) or settings.SECRET_KEY
    header_b64 = _b64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    body_b64 = _b64url_encode(json.dumps(body, separators=(',', ':')).encode('utf-8'))
    signing_input = f"{header_b64}.{body_b64}".encode('utf-8')
    signature = _sign(signing_input, secret)
    return f"{header_b64}.{body_b64}.{signature}"


def decode(token: str) -> Optional[Dict[str, Any]]:
    try:
        header_b64, body_b64, signature = token.split('.')
    except ValueError:
        return None
    secret = getattr(settings, 'AUTH_JWT_SECRET', None) or settings.SECRET_KEY
    expected_sig = _sign(f"{header_b64}.{body_b64}".encode('utf-8'), secret)
    if not hmac.compare_digest(signature, expected_sig):
        return None
    try:
        body = json.loads(_b64url_decode(body_b64).decode('utf-8'))
    except Exception:
        return None
    if 'exp' in body and int(time.time()) > int(body['exp']):
        return None
    return body


def company_id_from_request(request) -> Optional[int]:
    auth = request.META.get('HTTP_AUTHORIZATION') or ''
    if not auth.startswith('Bearer '):
        return None
    payload = decode(auth[len('Bearer '):])
    try:
        return int(payload.get('company_id')) if payload else None
    except Exception:
        return None


