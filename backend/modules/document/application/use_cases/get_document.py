from dataclasses import dataclass
from ..dtos import DocumentDTO
from ..ports import DocumentQueryRepository


@dataclass
class GetDocumentUseCase:
    document_repository: DocumentQueryRepository

    def execute(self, document_id: int) -> DocumentDTO | None:
        return self.document_repository.get_by_id(document_id)


