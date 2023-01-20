from datetime import timedelta

from app.inner.model.entities.file_document import FileDocument
from app.outer.interfaces.deliveries.contracts.requests.document_search.document_search_request import \
    DocumentSearchRequest
from app.outer.interfaces.deliveries.contracts.responses.document_search.document_search_response import \
    DocumentSearchResponse


class InFileSearch:
    def search(self, search_request: DocumentSearchRequest) -> DocumentSearchResponse[FileDocument]:
        response = DocumentSearchResponse(
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
