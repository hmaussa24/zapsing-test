from typing import Protocol, Optional
from .dtos import AnalysisResultDTO


class AnalysisResultCommandRepository(Protocol):
    def upsert(self, dto: AnalysisResultDTO) -> AnalysisResultDTO: ...


class AnalysisResultQueryRepository(Protocol):
    def get_by_document_id(self, document_id: int) -> Optional[AnalysisResultDTO]: ...


class AutomationNotifier(Protocol):
    def notify_document_created(self, *, document_id: int, company_id: int, name: str, pdf_url: str) -> None: ...

