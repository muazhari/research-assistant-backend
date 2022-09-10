from app.infrastucture.delivery.contract.request.document_transfer.document_transfer_upload_request import \
    DocumentUploadRequest


class DocumentWebUploadRequest(DocumentUploadRequest):
    url: str
