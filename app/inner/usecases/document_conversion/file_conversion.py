from app.inner.model.entities.file_document import FileDocument
from app.outer.interfaces.deliveries.contracts.responses.document_search.document_search_response import DocumentSearchResponse
from app.outer.utility.java_bytes import b64_encode


def convert_to_file(search_request, result):
    processed_document = FileDocument(
        name="processed document",
        description="processed description",
        account_id=search_request.account_id,
        file_name="processed file name",
        file_extension="pfe",
        file_bytes=b64_encode("processed file bytes"),
    )
    response = DocumentSearchResponse(
        processed_document=processed_document,
        process_duration=0
    )

    return response
