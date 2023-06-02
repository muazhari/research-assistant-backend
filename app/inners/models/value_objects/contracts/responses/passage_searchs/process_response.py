from typing import Union, List

from app.inners.models.value_objects.contracts.responses.base_response import BaseResponse
from app.inners.models.value_objects.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse


class ProcessResponse(BaseResponse):
    retrieved_documents: List[RetrievedDocumentResponse]
    output_document: Union[TextDocumentResponse, FileDocumentResponse, WebDocumentResponse]
    process_duration: float
