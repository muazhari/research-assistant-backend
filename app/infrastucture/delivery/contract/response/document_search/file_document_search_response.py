from app.core.model.entity.file_document import FileDocument
from app.infrastucture.delivery.contract.response.document_search.base_document_search_response import \
    BaseDocumentSearchResponse


class FileDocumentSearchResponse(BaseDocumentSearchResponse):
    processed_file_document: FileDocument
