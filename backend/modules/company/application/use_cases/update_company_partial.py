from dataclasses import dataclass
from typing import Any
from modules.company.application.dtos import CompanyDTO
from modules.company.application.ports import CompanyCommandRepository


@dataclass
class UpdateCompanyPartialUseCase:
    repo: CompanyCommandRepository

    def execute(self, company_id: int, **fields: Any) -> CompanyDTO | None:
        return self.repo.update_partial(company_id, **fields)


