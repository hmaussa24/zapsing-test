from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from modules.analysis.application.dtos import AnalysisResultDTO
from modules.analysis.application.ports import AnalysisResultCommandRepository, AnalysisResultQueryRepository


@dataclass
class HandleAnalysisWebhookUseCase:
    analysis_commands: AnalysisResultCommandRepository
    analysis_queries: AnalysisResultQueryRepository

    def execute(self, payload: dict) -> Optional[AnalysisResultDTO]:
        document_id = payload.get('document_id')
        if not document_id:
            raise ValueError('Missing document_id')

        def to_list_str(v) -> List[str]:
            return [str(x) for x in v] if isinstance(v, list) else []

        def to_list_any(v) -> List[Dict[str, Any]]:
            return v if isinstance(v, list) else []

        dto = AnalysisResultDTO(
            document_id=int(document_id),
            summary=str(payload.get('summary', '')).strip(),
            labels=to_list_str(payload.get('labels', [])),
            entities=to_list_any(payload.get('entities', [])),
            risk_score=float(payload.get('risk_score') or 0.0),
            status=(payload.get('status') or None),
            missing_topics=str(payload.get('missing_topics', 'no definidos')),
            insights=str(payload.get('insights', 'no definidos')),
            model_info=(payload.get('model_info') or {}),
        )

        existing = self.analysis_queries.get_by_document_id(dto.document_id)
        if existing and existing == dto:
            return existing

        return self.analysis_commands.upsert(dto)

