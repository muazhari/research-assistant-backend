from uuid import UUID

from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class DocumentSearchResponse(BaseRequest):
    process_duration: float
    processed_document_id: UUID
    evaluation_performance: float
