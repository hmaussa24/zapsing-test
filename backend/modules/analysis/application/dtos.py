from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class AnalysisResultDTO:
    document_id: int
    summary: str
    labels: List[str]
    entities: List[Dict[str, Any]]
    risk_score: float
    status: Optional[str] = None
    missing_topics: List[Dict[str, Any]] = None  # list de objetos topic/importance/suggestion...
    insights: List[Dict[str, Any]] = None       # list de hallazgos
    model_info: Dict[str, Any] = None           # metadatos del modelo

