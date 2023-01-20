
from uuid import UUID

from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class PassageSearchRequest(BaseRequest):
    account_id: UUID
    document_id: UUID
    query: str
    conversion_document_type_id: UUID
    granularity: str
    window_size: int
    retriever_model: str
    processed_name: str
    processed_description: str
