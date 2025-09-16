from dataclasses import dataclass
from ..dtos import CreateCompanyDTO, CompanyDTO
from ..ports import CompanyRepository


@dataclass
class CreateCompanyUseCase:
    company_repository: CompanyRepository

    def execute(self, dto: CreateCompanyDTO) -> CompanyDTO:
        return self.company_repository.create(name=dto.name, api_token=dto.api_token)


