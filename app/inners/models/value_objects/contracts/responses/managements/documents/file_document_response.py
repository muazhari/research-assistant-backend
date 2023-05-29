from app.inners.models.value_objects.contracts.responses.managements.documents.document_response import DocumentResponse


class FileDocumentResponse(DocumentResponse):
    file_name: str
    file_extension: str
    file_bytes: bytes
