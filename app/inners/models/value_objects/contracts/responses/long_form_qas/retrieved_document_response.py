from typing import List

from app.inners.models.value_objects.contracts.responses.base_response import BaseResponse


class RetrievedDocumentResponse(BaseResponse):
    id: str
    content: str
    content_type: str
    meta: dict
    id_hash_keys: List[str]
    score: float
