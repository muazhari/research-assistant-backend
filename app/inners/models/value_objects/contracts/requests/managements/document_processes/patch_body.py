from uuid import UUID

from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class PatchBody(BaseRequest):
    initial_document_id: UUID
    final_document_id: UUID
    process_duration: float
