from uuid import UUID

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest


class PatchBody(BaseRequest):
    name: str
    description: str
    document_type_id: UUID
    account_id: UUID
    text_content: str
