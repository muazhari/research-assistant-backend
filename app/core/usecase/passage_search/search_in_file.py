from datetime import timedelta, datetime

from app.core.model.entity.file_document import FileDocument
from app.infrastucture.delivery.contract.request.document_search.document_search_request import DocumentSearchRequest
from app.infrastucture.delivery.contract.response.document_search.base_document_search_response import BaseDocumentSearchResponse


def search_passage_in_file(search_request: DocumentSearchRequest) -> BaseDocumentSearchResponse:
    response = BaseDocumentSearchResponse(
        processed_corpus=FileDocument(
            id=2,
            document_id=2,
            file_name="file_name",
            file_extension="file_extension",
            file_byte=b"file",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        process_duration=timedelta(seconds=1)
    )

    return response
