from app.outer.interfaces.deliveries.contracts.requests.document_transfer.document_transfer_upload_request import \
    DocumentUploadRequest


class DocumentFileUploadRequest(DocumentUploadRequest):
    file_name: str
    file_extension: str
    file: bytes
