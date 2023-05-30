from pathlib import Path

from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.managements.file_documents.read_one_by_id_request import \
    ReadOneByIdRequest as FileDocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.read_one_by_id_request import \
    ReadOneByIdRequest as TextDocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.web_documents.read_one_by_id_request import \
    ReadOneByIdRequest as WebDocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.web_document_response import \
    WebDocumentResponse
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.inners.use_cases.managements.file_document_management import FileDocumentManagement
from app.inners.use_cases.managements.text_document_management import TextDocumentManagement
from app.inners.use_cases.managements.web_document_management import WebDocumentManagement


class BaseDocumentConversion:

    def __init__(self):

        self.document_management = DocumentManagement()
        self.document_type_management = DocumentTypeManagement()
        self.file_document_management = FileDocumentManagement()
        self.text_document_management = TextDocumentManagement()
        self.web_document_management = WebDocumentManagement()

    async def convert_document_to_corpus(self, document: Document, document_type: DocumentType) -> str:
        if document_type.name == "file":
            found_detail_document: Content[FileDocumentResponse] = await self.file_document_management.read_one_by_id(
                request=FileDocumentReadOneByIdRequest(
                    id=document.id
                )
            )
            file_name: str = found_detail_document.data.file_name
            file_extension: str = found_detail_document.data.file_extension
            file_path: Path = Path(f"app/outers/persistences/temps/{document.id}_{file_name}{file_extension}")
            file_bytes: bytes = found_detail_document.data.file_bytes
            with open(file_path, "wb") as file:
                file.write(file_bytes)
            corpus = file_path
        elif document_type.name == "text":
            found_detail_document: Content[TextDocumentResponse] = await self.text_document_management.read_one_by_id(
                request=TextDocumentReadOneByIdRequest(
                    id=document.id
                )
            )
            corpus = found_detail_document.data.text_content
        elif document_type.name == "web":
            found_detail_document: Content[WebDocumentResponse] = await self.web_document_management.read_one_by_id(
                request=WebDocumentReadOneByIdRequest(
                    id=document.id
                )
            )
            corpus = found_detail_document.data.web_url
        else:
            raise Exception(f"Document type {document_type.name} not yet supported.")

        return corpus
