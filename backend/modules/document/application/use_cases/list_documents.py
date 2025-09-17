from dataclasses import dataclass
from typing import Optional

from ..dtos import DocumentDTO, PageDTO
from ..ports import DocumentQueryRepository, ListDocumentsQuery


@dataclass
class ListDocumentsUseCase:
    document_repository: DocumentQueryRepository

    def execute(self, *, company_id: Optional[int] = None, page: int = 1, page_size: int = 10, order_by: str = 'created_at', order_dir: str = 'desc') -> PageDTO:
        query = ListDocumentsQuery(
            company_id=company_id,
            page=page,
            page_size=page_size,
            order_by=order_by,
            order_dir=order_dir,
        )
        return self.document_repository.list_paginated(query)


