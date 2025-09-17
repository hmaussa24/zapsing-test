from modules.company.domain.entities import Company as DomainCompany
from modules.company.application.dtos import CompanyDTO
from modules.company.infrastructure.django_app.models import Company as ORMCompany


def orm_to_dto(orm: ORMCompany) -> CompanyDTO:
    return CompanyDTO(id=orm.id, name=orm.name, api_token=orm.api_token)


def dto_to_domain(dto: CompanyDTO) -> DomainCompany:
    return DomainCompany(id=dto.id, name=dto.name, api_token=dto.api_token)


