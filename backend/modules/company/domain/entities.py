from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Company:
    id: Optional[int]
    name: str
    api_token: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(name: str, api_token: str) -> "Company":
        normalized_name = Company._normalize_name(name)
        normalized_token = Company._normalize_token(api_token)
        return Company(id=None, name=normalized_name, api_token=normalized_token)

    @staticmethod
    def _normalize_name(value: str) -> str:
        v = (value or '').strip()
        v = ' '.join(v.split())
        if not v:
            raise ValueError('Company.name is required')
        if len(v) > 255:
            raise ValueError('Company.name max length is 255')
        return v

    @staticmethod
    def _normalize_token(value: str) -> str:
        v = (value or '').strip()
        if not v:
            raise ValueError('Company.api_token is required')
        if len(v) > 255:
            raise ValueError('Company.api_token max length is 255')
        return v

    def rename(self, new_name: str) -> None:
        self.name = Company._normalize_name(new_name)

    def rotate_token(self, new_token: str) -> None:
        self.api_token = Company._normalize_token(new_token)


