from datetime import datetime
from typing import List, Dict, Any

from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse


class ProcessResponse(BaseResponse):
    re_ranked_documents: List[Dict[str, Any]]
    generated_answer: str
    started_at: datetime
    finished_at: datetime
