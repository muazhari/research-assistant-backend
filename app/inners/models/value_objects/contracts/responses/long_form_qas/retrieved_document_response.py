from app.inners.models.value_objects.contracts.responses.base_response import BaseResponse


class RetrievedDocumentResponse(BaseResponse):
    id: str
    content: str
    content_type: str
    meta: dict
    score: float
