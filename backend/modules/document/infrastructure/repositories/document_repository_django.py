from modules.document.application.ports import DocumentRepository
from modules.document.application.dtos import DocumentDTO
from modules.document.infrastructure.django_app.models import Document


class DjangoDocumentRepository(DocumentRepository):
    def create(self, company_id: int, name: str, pdf_url: str) -> DocumentDTO:
        obj = Document.objects.create(company_id=company_id, name=name, pdf_url=pdf_url)
        return DocumentDTO(id=obj.id, company_id=obj.company_id, name=obj.name, pdf_url=obj.pdf_url, status=obj.status, open_id=obj.open_id, token=obj.token, created_at=obj.created_at)

    def get_by_id(self, document_id: int) -> DocumentDTO | None:
        try:
            obj = Document.objects.get(id=document_id)
        except Document.DoesNotExist:  # type: ignore[attr-defined]
            return None
        return DocumentDTO(id=obj.id, company_id=obj.company_id, name=obj.name, pdf_url=obj.pdf_url, status=obj.status, open_id=obj.open_id, token=obj.token, created_at=obj.created_at)

    def list_all(self) -> list[DocumentDTO]:
        return [
            DocumentDTO(id=o.id, company_id=o.company_id, name=o.name, pdf_url=o.pdf_url, status=o.status, open_id=o.open_id, token=o.token, created_at=o.created_at)
            for o in Document.objects.all().order_by('-created_at')
        ]

    def update_partial(self, document_id: int, **fields) -> DocumentDTO | None:
        try:
            obj = Document.objects.get(id=document_id)
        except Document.DoesNotExist:  # type: ignore[attr-defined]
            return None
        for k, v in fields.items():
            setattr(obj, k, v)
        obj.save(update_fields=list(fields.keys()))
        return DocumentDTO(id=obj.id, company_id=obj.company_id, name=obj.name, pdf_url=obj.pdf_url, status=obj.status, open_id=obj.open_id, token=obj.token)

    def delete(self, document_id: int) -> bool:
        deleted, _ = Document.objects.filter(id=document_id).delete()
        return deleted > 0

    def list_by_company(self, company_id: int) -> list[DocumentDTO]:
        qs = Document.objects.filter(company_id=company_id).order_by('-created_at')
        return [
            DocumentDTO(id=o.id, company_id=o.company_id, name=o.name, pdf_url=o.pdf_url,
                         status=o.status, open_id=o.open_id, token=o.token, created_at=o.created_at)
            for o in qs
        ]


