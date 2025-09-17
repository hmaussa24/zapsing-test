from dataclasses import dataclass
from ..ports import DocumentRepository


@dataclass
class DeleteDocumentUseCase:
    document_repository: DocumentRepository

    def execute(self, document_id: int) -> bool:
        return self.document_repository.delete(document_id)


