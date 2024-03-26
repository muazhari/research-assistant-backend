from typing import Union, List

from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse
from apps.inners.models.dtos.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedChunkResponse
from apps.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from apps.inners.models.dtos.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse


class ProcessResponse(BaseResponse):
    retrieved_chunks: List[RetrievedChunkResponse]
    output_document: Union[TextDocumentResponse, FileDocumentResponse]
    document_process: DocumentProcess
