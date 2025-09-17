from modules.document.domain.entities import Document as DomainDocument
from modules.document.application.dtos import DocumentDTO
from modules.document.infrastructure.django_app.models import Document as ORMDocument


def orm_to_dto(orm: ORMDocument) -> DocumentDTO:
    return DocumentDTO(
        id=orm.id,
        company_id=orm.company_id,
        name=orm.name,
        pdf_url=orm.pdf_url,
        status=orm.status,
        open_id=orm.open_id,
        token=orm.token,
        created_at=orm.created_at,
        has_analysis=getattr(orm, 'has_analysis', None),
        risk_score=getattr(orm, 'risk_score', None),
    )


def dto_to_domain(dto: DocumentDTO) -> DomainDocument:
    return DomainDocument(
        id=dto.id,
        company_id=dto.company_id,
        name=dto.name,
        pdf_url=dto.pdf_url,
        status=dto.status,
        open_id=dto.open_id,
        token=dto.token,
        created_at=dto.created_at,
    )


