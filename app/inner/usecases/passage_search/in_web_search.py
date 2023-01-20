from datetime import timedelta

from app.inner.model.entities.web_document import WebDocument
from app.outer.interfaces.deliveries.contracts.requests.document_search.document_search_request import \
    DocumentSearchRequest
from app.outer.interfaces.deliveries.contracts.responses.document_search.document_search_response import \
    DocumentSearchResponse


class InWebSearch:
    def search(self, search_request: DocumentSearchRequest) -> DocumentSearchResponse[WebDocument]:
        response = DocumentSearchResponse(
            processed_corpus=WebDocument(
                id=1,
                document_id=1,
                web_url="https://www.google.com",
            ),
            process_duration=timedelta(seconds=1)
        )

        return response


in_web_search = InWebSearch()
