from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class SignerDTO:
    id: int
    document_id: int
    name: str
    email: str
    created_at: Optional[datetime] = None


@dataclass
class CreateSignerDTO:
    document_id: int
    name: str
    email: str


