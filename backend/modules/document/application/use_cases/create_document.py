from dataclasses import dataclass
from typing import Optional
from ..dtos import CreateDocumentDTO, DocumentDTO
from ..ports import DocumentCommandRepository, ZapSignClient
from modules.company.application.ports import CompanyQueryRepository
from modules.analysis.application.ports import AutomationNotifier
from modules.automation.application.ports import EventPublisher
from modules.automation.application.dtos import DocumentCreatedEvent


@dataclass
class CreateDocumentUseCase:
    document_repository: DocumentCommandRepository
    company_repository: Optional[CompanyQueryRepository] = None
    zap_sign_client: Optional[ZapSignClient] = None
    automation_notifier: Optional[AutomationNotifier] = None
    event_publisher: Optional[EventPublisher] = None

    def execute(self, dto: CreateDocumentDTO) -> DocumentDTO:
        doc = self.document_repository.create(company_id=dto.company_id, name=dto.name, pdf_url=dto.pdf_url)

        # Publicar evento a la cola (best-effort)
        if self.event_publisher:
            try:
                self.event_publisher.publish_document_created(DocumentCreatedEvent(
                    document_id=doc.id,  # type: ignore[arg-type]
                    company_id=dto.company_id,
                    name=dto.name,
                    pdf_url=dto.pdf_url,
                ))
            except Exception:
                pass

        # Best-effort: notificar a n8n (no bloquear si falla)
        if self.automation_notifier:
            try:
                self.automation_notifier.notify_document_created(
                    document_id=doc.id,  # type: ignore[arg-type]
                    company_id=dto.company_id,
                    name=dto.name,
                    pdf_url=dto.pdf_url,
                )
            except Exception:
                pass

        # Si no se inyectan dependencias externas, terminar aquí (permite tests unitarios sin mocks)
        if not self.company_repository or not self.zap_sign_client:
            return doc

        company = self.company_repository.get_by_id(dto.company_id)
        if not company:
            return doc

        result = None  # integración de creación en ZapSign no usada aquí
        return doc


