from app.core.model.entity.web_document import WebDocument
from app.infrastucture.delivery.contract.response.document_search.base_document_search_response import BaseDocumentSearchResponse


class WebDocumentSearchResponse(BaseDocumentSearchResponse):
    processed_web_document: WebDocument
