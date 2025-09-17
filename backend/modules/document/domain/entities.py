from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Document:
    id: Optional[int]
    company_id: int
    name: str
    pdf_url: str
    status: str = "created"
    open_id: Optional[str] = None
    token: Optional[str] = None
    created_at: Optional[datetime] = None

    @staticmethod
    def create(company_id: int, name: str, pdf_url: str) -> "Document":
        normalized_name = (name or "").strip()
        normalized_pdf_url = (pdf_url or "").strip()
        if not normalized_name:
            raise ValueError("Document.name is required")
        if len(normalized_name) > 200:
            raise ValueError("Document.name max length is 200")
        if not normalized_pdf_url:
            raise ValueError("Document.pdf_url is required")
        if len(normalized_pdf_url) > 4096:
            raise ValueError("Document.pdf_url max length is 4096")
        return Document(
            id=None,
            company_id=company_id,
            name=normalized_name,
            pdf_url=normalized_pdf_url,
        )


