from dataclasses import dataclass
from ..dtos import DocumentDTO
from ..ports import DocumentRepository


@dataclass
class GetDocumentUseCase:
    document_repository: DocumentRepository

    def execute(self, document_id: int) -> DocumentDTO | None:
        return self.document_repository.get_by_id(document_id)


