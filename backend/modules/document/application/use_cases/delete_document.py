from dataclasses import dataclass
from ..ports import DocumentCommandRepository


@dataclass
class DeleteDocumentUseCase:
    document_repository: DocumentCommandRepository

    def execute(self, document_id: int) -> bool:
        return self.document_repository.delete(document_id)


