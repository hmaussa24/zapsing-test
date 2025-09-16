from typing import Protocol, Optional

import pytest


# Estas importaciones fallarán hasta que implementemos los módulos
from modules.company.application.use_cases.create_company import (
    CreateCompanyUseCase,
)
from modules.company.application.dtos import CreateCompanyDTO, CompanyDTO
from modules.company.application.ports import CompanyRepository


class InMemoryCompanyRepository(CompanyRepository):
    def __init__(self) -> None:
        self._items = []
        self._auto_id = 1

    def create(self, name: str, api_token: str) -> CompanyDTO:
        company = CompanyDTO(id=self._auto_id, name=name, api_token=api_token)
        self._items.append(company)
        self._auto_id += 1
        return company

    def get_by_id(self, company_id: int) -> Optional[CompanyDTO]:
        return next((c for c in self._items if c.id == company_id), None)


def test_create_company_use_case_creates_and_returns_company():
    repo = InMemoryCompanyRepository()
    use_case = CreateCompanyUseCase(company_repository=repo)

    dto_in = CreateCompanyDTO(name="Acme Corp", api_token="token-123")
    result = use_case.execute(dto_in)

    assert isinstance(result, CompanyDTO)
    assert result.id == 1
    assert result.name == "Acme Corp"
    assert result.api_token == "token-123"


