from typing import Protocol, Optional
from .dtos import CompanyDTO


class CompanyCommandRepository(Protocol):
    def create(self, name: str, api_token: str) -> CompanyDTO: ...
    def update_partial(self, company_id: int, **fields) -> Optional[CompanyDTO]: ...
    def delete(self, company_id: int) -> bool: ...


class CompanyQueryRepository(Protocol):
    def get_by_id(self, company_id: int) -> Optional[CompanyDTO]: ...
    def list_all(self) -> list[CompanyDTO]: ...


class CompanyRepository(CompanyCommandRepository, CompanyQueryRepository, Protocol):
    """Compatibilidad retro con tests que importan CompanyRepository."""
    pass


