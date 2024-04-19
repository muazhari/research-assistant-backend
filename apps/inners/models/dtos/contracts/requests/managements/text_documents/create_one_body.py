from uuid import UUID

from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class CreateOneBody(BaseRequest):
    name: str
    description: str
    account_id: UUID
    text_content: str
