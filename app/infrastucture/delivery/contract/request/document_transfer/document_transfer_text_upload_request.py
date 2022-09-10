from app.infrastucture.delivery.contract.request.document_transfer.document_transfer_upload_request import \
    DocumentUploadRequest


class DocumentTextUploadRequest(DocumentUploadRequest):
    text: str
