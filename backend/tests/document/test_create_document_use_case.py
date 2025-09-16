import pytest

from modules.document.application.dtos import CreateDocumentDTO, DocumentDTO
from modules.document.application.ports import DocumentRepository
from modules.document.application.use_cases.create_document import CreateDocumentUseCase


class InMemoryDocumentRepository(DocumentRepository):
    def __init__(self) -> None:
        self._items: list[DocumentDTO] = []
        self._auto_id = 1

    def create(self, company_id: int, name: str, pdf_url: str) -> DocumentDTO:
        doc = DocumentDTO(id=self._auto_id, company_id=company_id, name=name, pdf_url=pdf_url, status="created", open_id=None, token=None)
        self._items.append(doc)
        self._auto_id += 1
        return doc

    def get_by_id(self, document_id: int) -> DocumentDTO | None:
        return next((d for d in self._items if d.id == document_id), None)


def test_create_document_use_case_creates_document():
    repo = InMemoryDocumentRepository()
    use_case = CreateDocumentUseCase(document_repository=repo)

    dto_in = CreateDocumentDTO(company_id=1, name="Contrato", pdf_url="https://example.com/doc.pdf")
    result = use_case.execute(dto_in)

    assert isinstance(result, DocumentDTO)
    assert result.id == 1
    assert result.name == "Contrato"
    assert result.pdf_url == "https://example.com/doc.pdf"
    assert result.company_id == 1
    assert result.status == "created"

