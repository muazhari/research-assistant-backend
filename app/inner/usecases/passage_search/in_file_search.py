from datetime import timedelta

from app.inner.model.entities.file_document import FileDocument
from app.outer.interfaces.deliveries.contracts.requests.passage_search.passage_search_request import \
    PassageSearchRequest
from app.outer.interfaces.deliveries.contracts.responses.passage_search.passage_search_response import \
    PassageSearchResponse


class InFileSearch:
    def search(self, search_request: PassageSearchRequest) -> PassageSearchResponse[FileDocument]:
        response = PassageSearchResponse(
            processed_corpus=FileDocument(
                id=2,
                document_id=2,
                file_name="file_name",
                file_extension="file_extension",
                file_byte=b"file"
            ),
            process_duration=timedelta(seconds=1)
        )

        return response


in_file_search = InFileSearch()
