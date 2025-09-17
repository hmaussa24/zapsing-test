from dataclasses import dataclass
from typing import Any
from ..dtos import DocumentDTO
from ..ports import DocumentCommandRepository


@dataclass
class UpdateDocumentPartialUseCase:
    document_repository: DocumentCommandRepository

    def execute(self, document_id: int, **fields: Any) -> DocumentDTO | None:
        return self.document_repository.update_partial(document_id, **fields)


