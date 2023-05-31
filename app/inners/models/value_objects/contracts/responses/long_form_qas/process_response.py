from typing import List

from app.inners.models.value_objects.contracts.responses.base_response import BaseResponse
from app.inners.models.value_objects.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedDocumentResponse


class ProcessResponse(BaseResponse):
    retrieved_documents: List[RetrievedDocumentResponse]
    generated_answer: str
    process_duration: float
