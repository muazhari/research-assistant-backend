from uuid import UUID

from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class DocumentUploadRequest(BaseRequest):
    account_id: UUID
    document_type_id: UUID
