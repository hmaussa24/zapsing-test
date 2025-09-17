from typing import Optional
import httpx
import logging
from django.conf import settings

from modules.document.application.dtos import ZapSignCreateResult
from modules.document.application.ports import ZapSignClient


logger = logging.getLogger(__name__)


class HttpZapSignClient(ZapSignClient):
    def __init__(self, base_url: Optional[str] = None, timeout_seconds: float = 15.0) -> None:
        self.base_url = (base_url or getattr(settings, 'ZAPSIGN_API_BASE', '')).rstrip('/')
        self.timeout_seconds = timeout_seconds
        self.auth_scheme = getattr(settings, 'ZAPSIGN_AUTH_SCHEME', 'Bearer')

    def create(self, api_token: str, name: str, pdf_url: str) -> ZapSignCreateResult:
        if not self.base_url or not api_token:
            logger.warning("ZapSign config incompleta: base_url o api_token ausente")
            logger.warning("base_url: %s", self.base_url)
            logger.warning("api_token: %s", api_token)
            return ZapSignCreateResult(open_id=None, token=None, status=None)

        url = f"{self.base_url}/docs/"
        headers = {
            'Authorization': f'{self.auth_scheme} {api_token}',
            'Content-Type': 'application/json',
        }
        # En la práctica ZapSign acepta 'url_pdf'; añadimos 'url' como fallback por compatibilidad
        payload = {
            'name': name,
            'url_pdf': pdf_url,
            'url': pdf_url,
            # ZapSign requiere 'signers'. Agregamos un signer por defecto configurable.
            'signers': [
                {
                    'name': getattr(settings, 'ZAPSIGN_DEFAULT_SIGNER_NAME', 'Default Signer'),
                    'email': getattr(settings, 'ZAPSIGN_DEFAULT_SIGNER_EMAIL', 'dev+signer@example.com'),
                }
            ],
        }
        def _mask(token: str) -> str:
            if not token:
                return ''
            return token[:4] + '...' + token[-4:]

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                resp = client.post(url, json=payload, headers=headers)
                body = None
                try:
                    body = resp.json()
                except Exception:
                    body = {'raw': resp.text[:500]}

                if resp.is_success:
                    # Intentar mapear múltiples posibles nombres de campos
                    open_id = body.get('open_id') or body.get('id') or body.get('openId')
                    token = body.get('token') or body.get('document_token') or body.get('doc_token')
                    status = body.get('status') or body.get('document_status')
                    if settings.DEBUG:
                        logger.info(
                            "ZapSign create OK status=%s body=%s",
                            resp.status_code,
                            body,
                        )
                    return ZapSignCreateResult(open_id=open_id, token=token, status=status)

                # Error HTTP
                logger.error(
                    "ZapSign create error status=%s url=%s body=%s headers=%s",
                    resp.status_code,
                    url,
                    body,
                    {**{k: v for k, v in headers.items() if k.lower() != 'authorization'}, 'Authorization': f"{self.auth_scheme} {_mask(api_token)}"},
                )
                return ZapSignCreateResult(open_id=None, token=None, status=None)
        except Exception as exc:
            logger.exception(
                "ZapSign create exception url=%s payload=%s headers=%s error=%s",
                url,
                payload,
                {**{k: v for k, v in headers.items() if k.lower() != 'authorization'}, 'Authorization': f"{self.auth_scheme} {_mask(api_token)}"},
                exc,
            )
            return ZapSignCreateResult(open_id=None, token=None, status=None)


