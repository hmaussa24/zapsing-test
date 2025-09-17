from dataclasses import dataclass


@dataclass
class DocumentCreatedEvent:
    document_id: int
    company_id: int
    name: str
    pdf_url: str

