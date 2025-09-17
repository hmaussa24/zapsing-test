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

        fields: dict = {}
        if status:
            fields['status'] = status
        if token:
            fields['token'] = token

        if not fields:
            return doc

        updated = self.document_commands.update_partial(doc.id, **fields)
        return updated or doc


