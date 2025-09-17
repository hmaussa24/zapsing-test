from modules.company.infrastructure.repositories.company_repository_django import DjangoCompanyRepository
from modules.company.application.use_cases.create_company import CreateCompanyUseCase
from modules.company.application.use_cases.list_companies import ListCompaniesUseCase
from modules.company.application.use_cases.get_company import GetCompanyUseCase
from modules.company.application.use_cases.update_company_partial import UpdateCompanyPartialUseCase
from modules.company.application.use_cases.delete_company import DeleteCompanyUseCase


def make_create_company_use_case() -> CreateCompanyUseCase:
    return CreateCompanyUseCase(company_repository=DjangoCompanyRepository())


def make_list_companies_use_case() -> ListCompaniesUseCase:
    return ListCompaniesUseCase(repo=DjangoCompanyRepository())


def make_get_company_use_case() -> GetCompanyUseCase:
    return GetCompanyUseCase(repo=DjangoCompanyRepository())


def make_update_company_partial_use_case() -> UpdateCompanyPartialUseCase:
    return UpdateCompanyPartialUseCase(repo=DjangoCompanyRepository())


def make_delete_company_use_case() -> DeleteCompanyUseCase:
    return DeleteCompanyUseCase(repo=DjangoCompanyRepository())


