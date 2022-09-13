from datetime import timedelta, datetime

from app.core.model.entity.file_document import FileDocument
from app.core.model.entity.web_document import WebDocument
from app.infrastucture.delivery.contract.request.document_search.document_search_request import DocumentSearchRequest
from app.infrastucture.delivery.contract.response.document_search.base_document_search_response import BaseDocumentSearchResponse


def search_passage_in_web(search_request: DocumentSearchRequest) -> BaseDocumentSearchResponse:
    response = BaseDocumentSearchResponse(
        processed_corpus=WebDocument(
            id=1,
            document_id=1,
            web_url="https://www.google.com",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        process_duration=timedelta(seconds=1)
    )

    return response
