from typing import Union, List

from app.inners.models.daos.document_process import DocumentProcess
from app.inners.models.dtos.contracts.responses.base_response import BaseResponse
from app.inners.models.dtos.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedChunkResponse
from app.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.inners.models.dtos.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse


class ProcessResponse(BaseResponse):
    retrieved_chunks: List[RetrievedChunkResponse]
    output_document: Union[TextDocumentResponse, FileDocumentResponse]
    document_process: DocumentProcess
