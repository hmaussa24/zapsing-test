from modules.document.application.ports import DocumentCommandRepository, DocumentQueryRepository, ListDocumentsQuery
from modules.document.application.dtos import DocumentDTO, PageDTO
from modules.document.infrastructure.django_app.models import Document
from modules.document.infrastructure.mappers import orm_to_dto


class DjangoDocumentRepository(DocumentCommandRepository, DocumentQueryRepository):
    def create(self, company_id: int, name: str, pdf_url: str) -> DocumentDTO:
        obj = Document.objects.create(company_id=company_id, name=name, pdf_url=pdf_url)
        return orm_to_dto(obj)

    def get_by_id(self, document_id: int) -> DocumentDTO | None:
        try:
            obj = Document.objects.get(id=document_id)
        except Document.DoesNotExist:  # type: ignore[attr-defined]
            return None
        return orm_to_dto(obj)

    def list_all(self) -> list[DocumentDTO]:
        return [orm_to_dto(o) for o in Document.objects.all().order_by('-created_at')]

    def update_partial(self, document_id: int, **fields) -> DocumentDTO | None:
        try:
            obj = Document.objects.get(id=document_id)
        except Document.DoesNotExist:  # type: ignore[attr-defined]
            return None
        for k, v in fields.items():
            setattr(obj, k, v)
        obj.save(update_fields=list(fields.keys()))
        return orm_to_dto(obj)

    def delete(self, document_id: int) -> bool:
        deleted, _ = Document.objects.filter(id=document_id).delete()
        return deleted > 0

    def list_by_company(self, company_id: int) -> list[DocumentDTO]:
        qs = Document.objects.filter(company_id=company_id).order_by('-created_at')
        return [orm_to_dto(o) for o in qs]

    def list_paginated(self, query: ListDocumentsQuery) -> PageDTO:
        qs = Document.objects.all()
        if query.company_id is not None:
            qs = qs.filter(company_id=query.company_id)
        order_field = query.order_by
        if query.order_dir == 'desc':
            order_field = f'-{order_field}'
        qs = qs.order_by(order_field)

        # paginación simple a nivel ORM
        total = qs.count()
        start = (query.page - 1) * query.page_size
        end = start + query.page_size
        items = [orm_to_dto(o) for o in qs[start:end]]

        # next/previous simples (sin construir URLs); DRF/adapter puede enriquecer
        next_token = None
        prev_token = None
        if end < total:
            next_token = 'next'
        if start > 0:
            prev_token = 'previous'

        return PageDTO(count=total, results=items, next=next_token, previous=prev_token)


