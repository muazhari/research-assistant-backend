from typing import List

from haystack import Document as HaystackDocument

from app.inners.models.value_objects.contracts.responses.base_response import BaseResponse


class ProcessResponse(BaseResponse):
    retrieved_documents: List[HaystackDocument]
    generated_answer: str
    process_duration: float
