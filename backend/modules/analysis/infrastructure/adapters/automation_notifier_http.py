from typing import Optional
import httpx
from django.conf import settings

from modules.analysis.application.ports import AutomationNotifier


class HttpAutomationNotifier(AutomationNotifier):
    def __init__(self, base_url: Optional[str] = None, timeout_seconds: float = 10.0) -> None:
        self.base_url = (base_url or getattr(settings, 'N8N_WEBHOOK_URL', '')).rstrip('/')
        self.timeout_seconds = timeout_seconds

    def notify_document_created(self, *, document_id: int, company_id: int, name: str, pdf_url: str) -> None:
        if not self.base_url:
            return
        headers = {
            'Content-Type': 'application/json',
            'X-Automation-Key': getattr(settings, 'AUTOMATION_API_KEY', ''),
        }
        body = {
            'event': 'document_created',
            'document': {
                'id': document_id,
                'company_id': company_id,
                'name': name,
                'pdf_url': pdf_url,
            }
        }
        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                client.post(self.base_url, json=body, headers=headers)
        except Exception:
            # Best-effort: no levantar excepción al flujo de creación
            return

