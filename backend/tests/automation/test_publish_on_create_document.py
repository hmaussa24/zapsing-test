from unittest.mock import Mock
from modules.document.application.use_cases.create_document import CreateDocumentUseCase
from modules.document.application.dtos import CreateDocumentDTO, DocumentDTO
from modules.document.application.ports import DocumentCommandRepository
from modules.automation.application.ports import EventPublisher
from modules.automation.application.dtos import DocumentCreatedEvent


class InMemoryDocRepo(DocumentCommandRepository):
    def __init__(self) -> None:
        self._id = 1

    def create(self, company_id: int, name: str, pdf_url: str) -> DocumentDTO:
        d = DocumentDTO(id=self._id, company_id=company_id, name=name, pdf_url=pdf_url, status='created')
        self._id += 1
        return d

    def update_partial(self, document_id: int, **fields):
        return None

    def delete(self, document_id: int) -> bool:
        return True


def test_publish_event_on_create_document():
    repo = InMemoryDocRepo()
    publisher = Mock(spec=EventPublisher)
    use_case = CreateDocumentUseCase(document_repository=repo)
    setattr(use_case, 'event_publisher', publisher)

    dto = CreateDocumentDTO(company_id=1, name='Doc', pdf_url='http://e.com/a.pdf')
    result = use_case.execute(dto)

    publisher.publish_document_created.assert_called_once_with(DocumentCreatedEvent(
        document_id=result.id, company_id=1, name='Doc', pdf_url='http://e.com/a.pdf'
    ))


