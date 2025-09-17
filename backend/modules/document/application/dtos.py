from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class DocumentDTO:
    id: int
    company_id: int
    name: str
    pdf_url: str
    status: str
    open_id: Optional[str] = None
    token: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class CreateDocumentDTO:
    company_id: int
    name: str
    pdf_url: str


@dataclass
class PageDTO:
    count: int
    results: list[DocumentDTO]
    next: Optional[str] = None
    previous: Optional[str] = None


@dataclass
class ZapSignCreateResult:
    open_id: Optional[str]
    token: Optional[str]
    status: Optional[str]


