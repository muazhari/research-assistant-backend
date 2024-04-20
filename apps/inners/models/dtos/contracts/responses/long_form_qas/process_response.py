from datetime import datetime
from typing import List

from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse
from apps.inners.models.dtos.contracts.responses.passage_searches.process_response import ReRankedDocument


class ProcessResponse(BaseResponse):
    re_ranked_documents: List[ReRankedDocument]
    generated_answer: str
    hallucination_grade: bool
    answer_relevancy_grade: bool
    started_at: datetime
    finished_at: datetime
