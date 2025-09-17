from dataclasses import dataclass
from modules.company.application.ports import CompanyCommandRepository


@dataclass
class DeleteCompanyUseCase:
    repo: CompanyCommandRepository

    def execute(self, company_id: int) -> bool:
        return self.repo.delete(company_id)


