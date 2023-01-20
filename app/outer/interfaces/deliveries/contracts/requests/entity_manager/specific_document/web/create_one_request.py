from uuid import UUID

from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class CreateOneRequest(BaseRequest):
    name: str
    description: str
    document_type_id: UUID
    account_id: UUID
    web_url: str
