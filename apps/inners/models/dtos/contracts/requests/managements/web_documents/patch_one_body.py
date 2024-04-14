from uuid import UUID

from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class PatchOneBody(BaseRequest):
    name: str
    description: str
    account_id: UUID
    web_url: str
