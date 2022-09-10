import uuid
from datetime import datetime, timedelta

from app.core.model.entity.document import Document
from app.core.model.entity.document_process import DocumentProcess
from app.core.model.entity.file_document import FileDocument
from app.core.model.entity.text_document import TextDocument
from app.core.model.entity.web_document import WebDocument
from app.core.usecase.crud import crud_account, crud_document, crud_document_type, crud_text_document, \
    crud_document_process
from app.infrastucture.delivery.contract.request.document_search.document_search_request import \
    DocumentSearchRequest
from app.infrastucture.delivery.contract.response.document_search.document_search_response import \
    DocumentSearchResponse


def search_passage_in_text(search_request: DocumentSearchRequest) -> DocumentSearchResponse:
    found_account = crud_account.find_one_by_id(search_request.account_id),
    found_document = crud_document.find_one_by_id(search_request.document_id),
    found_conversion_document_type = crud_document_type.find_one_by_id(
        search_request.conversion_document_type_id)

    document_to_create = Document(
        id=uuid.uuid4(),
        account_id=found_account[0].id,
        document_type_id=found_conversion_document_type.id,
        name="text document name",
        description="text document description",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    created_document = crud_document.create_one(document_to_create)

    text_document_to_create = TextDocument(
        id=uuid.uuid4(),
        document_id=created_document.id,
        text_content="text @123",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    created_text_document = crud_text_document.create_one(text_document_to_create)

    document_process = DocumentProcess(
        id=uuid.uuid4(),
        from_document_id=found_document[0].id,
        to_document_id=created_document.id,
        process_duration=1000,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    created_document_process = crud_document_process.create_one(document_process)

    response = DocumentSearchResponse(
        processed_document=created_text_document,
        process_duration=created_document_process.process_duration
    )

    return response


def search_passage_in_file(search_request: DocumentSearchRequest) -> DocumentSearchResponse:
    response = DocumentSearchResponse(
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


def search_passage_in_web(search_request: DocumentSearchRequest) -> DocumentSearchResponse:
    response = DocumentSearchResponse(
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
