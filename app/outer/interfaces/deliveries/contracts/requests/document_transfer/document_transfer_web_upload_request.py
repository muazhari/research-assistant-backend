from app.outer.interfaces.deliveries.contracts.requests.document_transfer.document_transfer_upload_request import \
    DocumentUploadRequest


class DocumentWebUploadRequest(DocumentUploadRequest):
    url: str
