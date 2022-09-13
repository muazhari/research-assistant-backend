import uuid
from uuid import UUID

from app.core.model.entity.document import Document
from app.core.model.entity.file_document import FileDocument
from app.core.model.entity.text_document import TextDocument
from app.core.model.entity.web_document import WebDocument


def create_text_document(name, description, account_id, text_content):
    document = Document(
        id=uuid.uuid4(),
        name=name,
        description=description,
        account_id=account_id,
        document_type_id=UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7560")
    )

    text_document = TextDocument(
        document_id=document.id,
        text_content=text_content,
    )
    return {"document": document, "text_document": text_document}


def create_file_document(name, description, account_id, file_name, file_extension, file_bytes):
    document = Document(
        id=uuid.uuid4(),
        name=name,
        description=description,
        account_id=account_id,
        document_type_id=UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7561")
    )

    file_document = FileDocument(
        document_id=document.id,
        file_name=file_name,
        file_extension=file_extension,
        file_bytes=file_bytes
    )
    return {"document": document, "file_document": file_document}


def create_web_document(name, description, account_id, web_url):
    document = Document(
        id=uuid.uuid4(),
        name=name,
        description=description,
        account_id=account_id,
        document_type_id=UUID("eb5adc50-df69-4bd0-b4d0-e300d3ff7562")
    )

    web_document = WebDocument(
        document_id=document.id,
        web_url=web_url,
    )
    return {"document": document, "web_document": web_document}
