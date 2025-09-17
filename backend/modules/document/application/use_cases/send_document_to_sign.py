from dataclasses import dataclass
from typing import Optional

from modules.document.application.dtos import DocumentDTO
from modules.document.application.ports import DocumentCommandRepository, DocumentQueryRepository, ZapSignClient
from modules.company.application.ports import CompanyQueryRepository
from modules.signer.application.ports import SignerQueryRepository


@dataclass
class SendDocumentToSignUseCase:
    document_commands: DocumentCommandRepository
    document_queries: DocumentQueryRepository
    company_queries: CompanyQueryRepository
    signer_queries: SignerQueryRepository
    zap_sign_client: ZapSignClient

    def execute(self, document_id: int) -> Optional[DocumentDTO]:
        doc = self.document_queries.get_by_id(document_id)
        if not doc:
            return None

        company = self.company_queries.get_by_id(doc.company_id)
        if not company or not company.api_token:
            return doc

        signers = self.signer_queries.list_by_document(document_id)
        if len(signers) == 0 or len(signers) > 2:
            raise Exception('Document must have 1 or 2 signers before sending')

        payload_signers = [{'name': s.name, 'email': s.email} for s in signers]

        result = self.zap_sign_client.send_for_sign(
            api_token=company.api_token,
            name=doc.name,
            pdf_url=doc.pdf_url,
            signers=payload_signers,
        )

        # Actualizar documento si hay datos relevantes
        fields: dict = {}
        if result.open_id:
            fields['open_id'] = result.open_id
        if result.token:
            fields['token'] = result.token
        if result.status:
            fields['status'] = result.status

        if fields:
            updated = self.document_commands.update_partial(document_id, **fields)
            if updated:
                return updated
        return doc


