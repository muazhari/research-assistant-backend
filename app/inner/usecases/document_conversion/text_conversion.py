import uuid
from datetime import datetime

from app.inner.model.entities.document import Document
from app.inner.model.entities.text_document import TextDocument
from app.outer.interfaces.deliveries.contracts.requests.document_search.document_search_request import \
    DocumentSearchRequest
from app.outer.interfaces.deliveries.contracts.responses.document_search.document_search_response import \
    DocumentSearchResponse


def convert_to_text(search_request: DocumentSearchRequest, result: str) -> DocumentSearchResponse[TextDocument]:
    document = Document(
        id=uuid.uuid4(),
        name=search_request.processed_name,
        description=search_request.processed_description,
        account_id=search_request.account_id,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )

    text_document = TextDocument(
        id=uuid.uuid4(),
        document_id=document.id,
        text_content=result
    )

    response = DocumentSearchResponse(
        processed_document=text_document,
        process_duration=0
    )

    return response
