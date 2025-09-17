from dataclasses import dataclass
from ..dtos import CreateSignerDTO, SignerDTO
from ..ports import SignerCommandRepository, SignerQueryRepository
from modules.signer.domain.entities import Signer


@dataclass
class AddSignerToDocumentUseCase:
    repo: SignerCommandRepository | SignerQueryRepository

    def execute(self, dto: CreateSignerDTO) -> SignerDTO:
        # Validaciones de dominio (normaliza nombre/email y valida formato)
        candidate = Signer.create(dto.document_id, dto.name, dto.email)

        # Límite máximo 2 por documento
        current = self.repo.count_by_document(dto.document_id)  # type: ignore[attr-defined]
        if current >= 2:
            raise Exception('Max 2 signers per document')

        # Unicidad por email en documento
        existing = self.repo.get_by_document_and_email(dto.document_id, candidate.email)  # type: ignore[attr-defined]
        if existing:
            raise Exception('Email already exists for this document')

        # Crear
        return self.repo.create(dto.document_id, candidate.name, candidate.email)  # type: ignore[attr-defined]


