from modules.document.application.ports import DocumentRepository
from modules.document.application.dtos import DocumentDTO
from modules.document.infrastructure.django_app.models import Document


class DjangoDocumentRepository(DocumentRepository):
    def create(self, company_id: int, name: str, pdf_url: str) -> DocumentDTO:
        obj = Document.objects.create(company_id=company_id, name=name, pdf_url=pdf_url)
        return DocumentDTO(id=obj.id, company_id=obj.company_id, name=obj.name, pdf_url=obj.pdf_url, status=obj.status, open_id=obj.open_id, token=obj.token)

    def get_by_id(self, document_id: int) -> DocumentDTO | None:
        try:
            obj = Document.objects.get(id=document_id)
        except Document.DoesNotExist:  # type: ignore[attr-defined]
            return None
        return DocumentDTO(id=obj.id, company_id=obj.company_id, name=obj.name, pdf_url=obj.pdf_url, status=obj.status, open_id=obj.open_id, token=obj.token)

    def list_all(self) -> list[DocumentDTO]:
        return [
            DocumentDTO(id=o.id, company_id=o.company_id, name=o.name, pdf_url=o.pdf_url, status=o.status, open_id=o.open_id, token=o.token)
            for o in Document.objects.all().order_by('id')
        ]


