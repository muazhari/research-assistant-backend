from typing import List

from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse
from apps.inners.models.dtos.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedChunkResponse


class ProcessResponse(BaseResponse):
    retrieved_chunks: List[RetrievedChunkResponse]
    generated_answer: str
    document_process: DocumentProcess
