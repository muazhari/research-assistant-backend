from uuid import UUID

from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class PatchOneByIdRequest(BaseRequest):
    document_id: UUID
    text_content: str
