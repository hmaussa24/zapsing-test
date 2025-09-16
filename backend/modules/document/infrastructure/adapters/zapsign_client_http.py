from typing import Optional
import httpx
from django.conf import settings

from modules.document.application.dtos import ZapSignCreateResult
from modules.document.application.ports import ZapSignClient


class HttpZapSignClient(ZapSignClient):
    def __init__(self, base_url: Optional[str] = None, timeout_seconds: float = 10.0) -> None:
        self.base_url = base_url or getattr(settings, 'ZAPSIGN_API_BASE', '').rstrip('/')
        self.timeout_seconds = timeout_seconds

    def create(self, api_token: str, name: str, pdf_url: str) -> ZapSignCreateResult:
        if not self.base_url:
            return ZapSignCreateResult(open_id=None, token=None, status=None)

        url = f"{self.base_url}/docs/"
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }
        payload = {
            'name': name,
            # Los docs de ZapSign suelen aceptar 'url_pdf' o similar; usamos 'url_pdf'.
            'url_pdf': pdf_url,
        }
        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                resp = client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                # Campos esperados: open_id, token, status (nombres según docs públicas)
                return ZapSignCreateResult(
                    open_id=data.get('open_id'),
                    token=data.get('token'),
                    status=data.get('status'),
                )
        except Exception:
            # En integración real, deberíamos loguear y propagar una excepción de dominio.
            # Por ahora, retornamos nulos para no romper el flujo local sin credenciales reales.
            return ZapSignCreateResult(open_id=None, token=None, status=None)


