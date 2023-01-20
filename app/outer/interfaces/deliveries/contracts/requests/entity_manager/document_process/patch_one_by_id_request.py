from uuid import UUID

from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class PatchOneByIdRequest(BaseRequest):
    initial_document_id: UUID
    final_document_id: UUID
    process_duration: float
