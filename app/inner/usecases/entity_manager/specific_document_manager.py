from app.inner.model.entities.document import Document
from app.inner.model.entities.file_document import FileDocument
from app.inner.model.entities.text_document import TextDocument
from app.inner.model.entities.web_document import WebDocument
from app.inner.model.value_objects.specific_document import SpecificDocument
from app.inner.usecases.entity_manager.document_manager import document_manager
from app.inner.usecases.entity_manager.file_document_manager import file_document_manager
from app.inner.usecases.entity_manager.text_document_manager import text_document_manager
from app.inner.usecases.entity_manager.web_document_manager import web_document_manager
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.document.create_one_request import \
    CreateOneRequest as DocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.file_document.create_one_request import \
    CreateOneRequest as FileDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.specific_document.file.create_one_request import \
    CreateOneRequest as FileSpecificDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.specific_document.text.create_one_request import \
    CreateOneRequest as TextSpecificDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.specific_document.web.create_one_request import \
    CreateOneRequest as WebSpecificDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.text_document.create_one_request import \
    CreateOneRequest as TextDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.web_document.create_one_request import \
    CreateOneRequest as WebDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.responses.content import Content


class SpecificDocumentManager:

    def create_one_file_document(self, file_document_specific_request: FileSpecificDocumentCreateOneRequest) -> \
            SpecificDocument[FileDocument]:
        document_request: DocumentCreateOneRequest = DocumentCreateOneRequest(
            name=file_document_specific_request.name,
            description=file_document_specific_request.description,
            account_id=file_document_specific_request.account_id,
            document_type_id=file_document_specific_request.document_type_id,
        )
        file_document_request: FileDocumentCreateOneRequest = FileDocumentCreateOneRequest(
            file_name=file_document_specific_request.file_name,
            file_extension=file_document_specific_request.file_extension,
            file_bytes=file_document_specific_request.file_bytes,
        )
        document: Content[Document] = document_manager.create_one(document_request)
        file_document_request.document_id = document.data.id
        file_document: Content[FileDocument] = file_document_manager.create_one(file_document_request)
        specific_document: SpecificDocument = SpecificDocument(
            document=document.data,
            document_detail=file_document.data
        )
        return specific_document

    def create_one_text_document(self, text_document_specific_request: TextSpecificDocumentCreateOneRequest) -> \
            SpecificDocument[TextDocument]:
        document_request: DocumentCreateOneRequest = DocumentCreateOneRequest(
            name=text_document_specific_request.name,
            description=text_document_specific_request.description,
            account_id=text_document_specific_request.account_id,
            document_type_id=text_document_specific_request.document_type_id,
        )
        text_document_request: TextDocumentCreateOneRequest = TextDocumentCreateOneRequest(
            text_content=text_document_specific_request.text_content,
        )
        document: Content[Document] = document_manager.create_one(document_request)
        text_document_request.document_id = document.data.id
        text_document: Content[TextDocument] = text_document_manager.create_one(text_document_request)
        specific_document: SpecificDocument = SpecificDocument(
            document=document.data,
            document_detail=text_document.data
        )
        return specific_document

    def create_one_web_document(self, web_document_specific_request: WebSpecificDocumentCreateOneRequest) -> \
            SpecificDocument[WebDocument]:
        document_request: DocumentCreateOneRequest = DocumentCreateOneRequest(
            name=web_document_specific_request.name,
            description=web_document_specific_request.description,
            account_id=web_document_specific_request.account_id,
            document_type_id=web_document_specific_request.document_type_id,
        )
        web_document_request: TextDocumentCreateOneRequest = WebDocumentCreateOneRequest(
            web_url=web_document_specific_request.web_url,
        )
        document: Content[Document] = document_manager.create_one(document_request)
        web_document_request.document_id = document.data.id
        web_document: Content[WebDocument] = web_document_manager.create_one(web_document_request)
        specific_document: SpecificDocument = SpecificDocument(
            document=document.data,
            document_detail=web_document.data
        )
        return specific_document


specific_document_manager = SpecificDocumentManager()
