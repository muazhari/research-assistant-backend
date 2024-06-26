from datetime import datetime
from uuid import UUID

from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class PatchOneBody(BaseRequest):
    initial_document_id: UUID
    final_document_id: UUID
    started_at: datetime
    finished_at: datetime
