from __future__ import annotations

from uuid import UUID

from app.inners.models.value_objects.contracts.responses.base_response import BaseResponse


class DocumentResponse(BaseResponse, table=True):
    id: UUID
    name: str
    description: str
    document_type_id: UUID
    account_id: UUID
