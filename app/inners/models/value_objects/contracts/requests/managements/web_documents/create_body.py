from uuid import UUID

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest


class CreateBody(BaseRequest):
    name: str
    description: str
    document_type_id: UUID
    account_id: UUID
    web_url: str
