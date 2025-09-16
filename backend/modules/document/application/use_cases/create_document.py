from dataclasses import dataclass
from ..dtos import CreateDocumentDTO, DocumentDTO
from ..ports import DocumentRepository


@dataclass
class CreateDocumentUseCase:
    document_repository: DocumentRepository

    def execute(self, dto: CreateDocumentDTO) -> DocumentDTO:
        return self.document_repository.create(company_id=dto.company_id, name=dto.name, pdf_url=dto.pdf_url)


