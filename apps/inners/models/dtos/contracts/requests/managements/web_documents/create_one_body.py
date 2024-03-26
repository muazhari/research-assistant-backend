from uuid import UUID

from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class CreateOneBody(BaseRequest):
    name: str
    description: str
    document_type_id: str
    account_id: UUID
    web_url: str
