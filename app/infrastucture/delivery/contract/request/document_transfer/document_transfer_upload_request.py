from uuid import UUID

from pydantic import BaseModel


class DocumentUploadRequest(BaseModel):
    account_id: UUID
    document_type_id: UUID
