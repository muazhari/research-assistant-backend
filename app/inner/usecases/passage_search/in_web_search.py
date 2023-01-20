from datetime import timedelta

from app.inner.model.entities.web_document import WebDocument
from app.outer.interfaces.deliveries.contracts.requests.passage_search.passage_search_request import \
    PassageSearchRequest
from app.outer.interfaces.deliveries.contracts.responses.passage_search.passage_search_response import \
    PassageSearchResponse


class InWebSearch:
    def search(self, search_request: PassageSearchRequest) -> PassageSearchResponse[WebDocument]:
        response = PassageSearchResponse(
            processed_corpus=WebDocument(
                id=1,
                document_id=1,
                web_url="https://www.google.com",
            ),
            process_duration=timedelta(seconds=1)
        )

        return response


in_web_search = InWebSearch()
