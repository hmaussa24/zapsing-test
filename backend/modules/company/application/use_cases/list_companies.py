from dataclasses import dataclass
from modules.company.application.dtos import CompanyDTO
from modules.company.application.ports import CompanyQueryRepository


@dataclass
class ListCompaniesUseCase:
    repo: CompanyQueryRepository

    def execute(self) -> list[CompanyDTO]:
        return self.repo.list_all()


