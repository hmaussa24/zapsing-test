from dataclasses import dataclass
from modules.company.application.dtos import CompanyDTO
from modules.company.application.ports import CompanyQueryRepository


@dataclass
class GetCompanyUseCase:
    repo: CompanyQueryRepository

    def execute(self, company_id: int) -> CompanyDTO | None:
        return self.repo.get_by_id(company_id)


