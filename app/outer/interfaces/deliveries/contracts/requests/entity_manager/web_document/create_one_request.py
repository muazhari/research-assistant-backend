from uuid import UUID

from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class CreateOneRequest(BaseRequest):
    document_id: UUID
    web_url: str
