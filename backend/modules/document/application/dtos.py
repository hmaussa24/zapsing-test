from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentDTO:
    id: int
    company_id: int
    name: str
    pdf_url: str
    status: str
    open_id: Optional[str] = None
    token: Optional[str] = None


@dataclass
class CreateDocumentDTO:
    company_id: int
    name: str
    pdf_url: str


@dataclass
class ZapSignCreateResult:
    open_id: Optional[str]
    token: Optional[str]
    status: Optional[str]


