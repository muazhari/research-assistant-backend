from typing import List

from app.inners.models.daos.document_process import DocumentProcess
from app.inners.models.dtos.contracts.responses.base_response import BaseResponse
from app.inners.models.dtos.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedChunkResponse


class ProcessResponse(BaseResponse):
    retrieved_chunks: List[RetrievedChunkResponse]
    generated_answer: str
    document_process: DocumentProcess
