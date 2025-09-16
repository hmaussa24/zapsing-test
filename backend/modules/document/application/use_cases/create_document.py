from dataclasses import dataclass
from typing import Optional
from ..dtos import CreateDocumentDTO, DocumentDTO
from ..ports import DocumentRepository, ZapSignClient
from modules.company.application.ports import CompanyRepository


@dataclass
class CreateDocumentUseCase:
    document_repository: DocumentRepository
    company_repository: Optional[CompanyRepository] = None
    zap_sign_client: Optional[ZapSignClient] = None

    def execute(self, dto: CreateDocumentDTO) -> DocumentDTO:
        doc = self.document_repository.create(company_id=dto.company_id, name=dto.name, pdf_url=dto.pdf_url)

        # Si no se inyectan dependencias externas, terminar aquí (permite tests unitarios sin mocks)
        if not self.company_repository or not self.zap_sign_client:
            return doc

        company = self.company_repository.get_by_id(dto.company_id)
        if not company:
            return doc

        result = self.zap_sign_client.create(api_token=company.api_token, name=dto.name, pdf_url=dto.pdf_url)

        if result.open_id or result.token or result.status:
            updated = self.document_repository.update_partial(
                doc.id,
                open_id=result.open_id,
                token=result.token,
                status=result.status or doc.status,
            )
            if updated:
                return updated
        return doc


