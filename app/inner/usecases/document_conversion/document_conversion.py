from app.inner.model.entities.file_document import FileDocument
from app.inner.model.entities.text_document import TextDocument
from app.inner.model.entities.web_document import WebDocument
from app.inner.model.value_objects.passage_search.file_passage_search_result import \
    FilePassageSearchResult
from app.inner.model.value_objects.specific_document import SpecificDocument
from app.inner.model.value_objects.passage_search.text_passage_search_result import \
    TextPassageSearchResult
from app.inner.model.value_objects.passage_search.web_passage_search_result import \
    WebPassageSearchResult
from app.inner.usecases.entity_manager.specific_document_manager import specific_document_manager
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.specific_document.file.create_one_request import \
    CreateOneRequest as FileSpecificDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.specific_document.text.create_one_request import \
    CreateOneRequest as TextSpecificDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.entity_manager.specific_document.web.create_one_request import \
    CreateOneRequest as WebSpecificDocumentCreateOneRequest
from app.outer.interfaces.deliveries.contracts.requests.passage_search.passage_search_request import \
    PassageSearchRequest


class DocumentConversion:

    def create_file_document(self, passage_search_request: PassageSearchRequest,
                             file_passage_search_result: FilePassageSearchResult) \
            -> SpecificDocument[FileDocument]:
        file_specific_document_request: FileSpecificDocumentCreateOneRequest = FileSpecificDocumentCreateOneRequest(
            name=passage_search_request.processed_name,
            description=passage_search_request.processed_description,
            account_id=passage_search_request.account_id,
            document_type_id=passage_search_request.conversion_document_type_id,
            file_name=file_passage_search_result.file_name,
            file_extension=file_passage_search_result.file_extension,
            file_bytes=file_passage_search_result.file_bytes,
        )
        specific_document = specific_document_manager.create_one_file_document(file_specific_document_request)
        return specific_document

    def create_text_document(self, passage_search_request: PassageSearchRequest,
                             text_passage_search_result: TextPassageSearchResult) \
            -> SpecificDocument[TextDocument]:
        text_specific_document_request: TextSpecificDocumentCreateOneRequest = TextSpecificDocumentCreateOneRequest(
            name=passage_search_request.processed_name,
            description=passage_search_request.processed_description,
            account_id=passage_search_request.account_id,
            document_type_id=passage_search_request.conversion_document_type_id,
            text_content=text_passage_search_result.text_content,
        )
        specific_document = specific_document_manager.create_one_text_document(text_specific_document_request)
        return specific_document

    def create_web_document(self, passage_search_request: PassageSearchRequest,
                            web_passage_search_result: WebPassageSearchResult) \
            -> SpecificDocument[WebDocument]:
        web_specific_document_request: WebSpecificDocumentCreateOneRequest = WebSpecificDocumentCreateOneRequest(
            name=passage_search_request.processed_name,
            description=passage_search_request.processed_description,
            account_id=passage_search_request.account_id,
            document_type_id=passage_search_request.conversion_document_type_id,
            web_url=web_passage_search_result.web_url,
        )
        specific_document = specific_document_manager.create_one_web_document(web_specific_document_request)
        return specific_document


document_conversion = DocumentConversion()
