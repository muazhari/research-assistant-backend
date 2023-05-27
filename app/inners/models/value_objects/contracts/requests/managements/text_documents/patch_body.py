from uuid import UUID

from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class PatchBody(BaseRequest):
    document_id: UUID
    text_content: str
