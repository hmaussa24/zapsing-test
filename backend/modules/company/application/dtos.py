from dataclasses import dataclass


@dataclass
class CompanyDTO:
    id: int
    name: str
    api_token: str


@dataclass
class CreateCompanyDTO:
    name: str
    api_token: str


