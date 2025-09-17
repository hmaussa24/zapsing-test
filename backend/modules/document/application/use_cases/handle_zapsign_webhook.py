from dataclasses import dataclass
from typing import Optional

from modules.document.application.dtos import DocumentDTO
from modules.document.application.ports import DocumentCommandRepository, DocumentQueryRepository


@dataclass
class HandleZapSignWebhookUseCase:
    document_commands: DocumentCommandRepository
    document_queries: DocumentQueryRepository

    def execute(self, payload: dict) -> Optional[DocumentDTO]:
        open_id = payload.get('open_id') or payload.get('id') or payload.get('openId')
        status = payload.get('status') or payload.get('document_status')
        token = payload.get('token') or payload.get('document_token')

        if not open_id:
            raise ValueError('Missing open_id')

        doc = self.document_queries.get_by_open_id(str(open_id))
        if not doc:
            return None

        # Idempotencia y progresión de estados (evitar regresiones y duplicados)
        def normalize(s: Optional[str]) -> Optional[str]:
            return s.lower() if isinstance(s, str) else s

        current_status = normalize(doc.status)
        incoming_status = normalize(status)

        status_rank = {
            None: -1,
            'created': 0,
            'ready': 1,
            'pending': 2,
            'sent': 3,
            'signed': 4,
            'completed': 5,
            'error': 99,
            'failed': 99,
        }

        should_update_status = False
        if incoming_status is not None:
            # Actualizar si es diferente y representa un avance o un estado terminal (error/failed)
            if incoming_status in ('error', 'failed'):
                should_update_status = current_status not in ('signed', 'completed') and current_status != incoming_status
            else:
                should_update_status = status_rank.get(incoming_status, -1) > status_rank.get(current_status, -1)

        fields: dict = {}
        if should_update_status and incoming_status:
            fields['status'] = incoming_status
        if token and token != doc.token:
            fields['token'] = token

        if not fields:
            # No hay cambios que aplicar → idempotente
            return doc

        updated = self.document_commands.update_partial(doc.id, **fields)
        return updated or doc


