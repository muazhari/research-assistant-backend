from uuid import UUID

from pydantic import BaseModel


class DocumentSearchRequest(BaseModel):
    account_id: UUID
    document_id: UUID
    query: str
    conversion_document_type_id: UUID
