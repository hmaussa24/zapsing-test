from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import re


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class Signer:
    id: Optional[int]
    document_id: int
    name: str
    email: str
    created_at: Optional[datetime] = None

    @staticmethod
    def create(document_id: int, name: str, email: str) -> "Signer":
        n = (name or '').strip()
        e = (email or '').strip().lower()
        if not n:
            raise ValueError('Signer.name is required')
        if len(n) > 200:
            raise ValueError('Signer.name max length is 200')
        if not e or not EMAIL_RE.match(e):
            raise ValueError('Signer.email invalid')
        return Signer(id=None, document_id=document_id, name=n, email=e)


