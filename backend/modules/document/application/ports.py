from typing import Protocol, Optional
from dataclasses import dataclass
from .dtos import DocumentDTO, ZapSignCreateResult, PageDTO


class DocumentCommandRepository(Protocol):
    def create(self, company_id: int, name: str, pdf_url: str) -> DocumentDTO: ...
    def update_partial(self, document_id: int, **fields) -> Optional[DocumentDTO]: ...
    def delete(self, document_id: int) -> bool: ...


class DocumentQueryRepository(Protocol):
    def get_by_id(self, document_id: int) -> Optional[DocumentDTO]: ...
    def get_by_open_id(self, open_id: str) -> Optional[DocumentDTO]: ...
    def list_all(self) -> list[DocumentDTO]: ...
    def list_by_company(self, company_id: int) -> list[DocumentDTO]: ...
    def list_paginated(self, query: 'ListDocumentsQuery') -> PageDTO: ...


class ZapSignClient(Protocol):
    def create(self, api_token: str, name: str, pdf_url: str) -> ZapSignCreateResult: ...
    def send_for_sign(self, api_token: str, name: str, pdf_url: str, signers: list[dict]) -> ZapSignCreateResult: ...


@dataclass
class ListDocumentsQuery:
    company_id: Optional[int] = None
    page: int = 1
    page_size: int = 10
    order_by: str = 'created_at'
    order_dir: str = 'desc'


class DocumentRepository(DocumentCommandRepository, DocumentQueryRepository, Protocol):
    """Compatibilidad retro con tests antiguos que importan DocumentRepository."""
    pass

