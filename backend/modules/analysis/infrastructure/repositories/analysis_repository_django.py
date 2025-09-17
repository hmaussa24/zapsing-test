from typing import Optional

from modules.analysis.application.dtos import AnalysisResultDTO
from modules.analysis.application.ports import AnalysisResultCommandRepository, AnalysisResultQueryRepository
from modules.analysis.infrastructure.django_app.models import DocumentAnalysis
from modules.document.infrastructure.django_app.models import Document


class DjangoAnalysisRepository(AnalysisResultCommandRepository, AnalysisResultQueryRepository):
    def upsert(self, dto: AnalysisResultDTO) -> AnalysisResultDTO:
        # Si el documento no existe, no persistimos pero devolvemos el DTO para evitar 500 en el webhook
        doc = Document.objects.filter(id=dto.document_id).first()  # type: ignore[attr-defined]
        if not doc:
            return dto
        obj, _ = DocumentAnalysis.objects.update_or_create(  # type: ignore[attr-defined]
            document=doc,
            defaults={
                'summary': dto.summary,
                'labels': dto.labels,
                'entities': dto.entities,
                'risk_score': dto.risk_score,
                'status': dto.status,
            }
        )
        return AnalysisResultDTO(
            document_id=obj.document_id,  # type: ignore[attr-defined]
            summary=obj.summary,
            labels=obj.labels,
            entities=obj.entities,
            risk_score=obj.risk_score,
            status=obj.status,
        )

    def get_by_document_id(self, document_id: int) -> Optional[AnalysisResultDTO]:
        try:
            obj = DocumentAnalysis.objects.get(document_id=document_id)  # type: ignore[attr-defined]
        except DocumentAnalysis.DoesNotExist:  # type: ignore[attr-defined]
            return None
        return AnalysisResultDTO(
            document_id=obj.document_id,  # type: ignore[attr-defined]
            summary=obj.summary,
            labels=obj.labels,
            entities=obj.entities,
            risk_score=obj.risk_score,
            status=obj.status,
        )

