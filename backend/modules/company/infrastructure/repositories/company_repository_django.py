from modules.company.application.ports import CompanyCommandRepository, CompanyQueryRepository
from modules.company.application.dtos import CompanyDTO
from modules.company.infrastructure.django_app.models import Company
from modules.company.infrastructure.mappers import orm_to_dto


class DjangoCompanyRepository(CompanyCommandRepository, CompanyQueryRepository):
    def create(self, name: str, api_token: str) -> CompanyDTO:
        obj = Company.objects.create(name=name, api_token=api_token)
        return orm_to_dto(obj)

    def get_by_id(self, company_id: int) -> CompanyDTO | None:
        try:
            obj = Company.objects.get(id=company_id)
        except Company.DoesNotExist:  # type: ignore[attr-defined]
            return None
        return orm_to_dto(obj)

    def list_all(self) -> list[CompanyDTO]:
        return [orm_to_dto(o) for o in Company.objects.all().order_by('id')]

    def update_partial(self, company_id: int, **fields) -> CompanyDTO | None:
        try:
            obj = Company.objects.get(id=company_id)
        except Company.DoesNotExist:  # type: ignore[attr-defined]
            return None
        for k, v in fields.items():
            setattr(obj, k, v)
        obj.save(update_fields=list(fields.keys()))
        return orm_to_dto(obj)

    def delete(self, company_id: int) -> bool:
        deleted, _ = Company.objects.filter(id=company_id).delete()
        return deleted > 0


