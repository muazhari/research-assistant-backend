from app.core.model.entity.text_document import TextDocument
from app.infrastucture.delivery.contract.response.document_search.base_document_search_response import BaseDocumentSearchResponse


class TextDocumentSearchResponse(BaseDocumentSearchResponse):
    processed_text_document: TextDocument
