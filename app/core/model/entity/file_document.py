from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.model.entity.base_entity import BaseEntity


class FileDocument(BaseEntity):
    id: Optional[UUID]
    document_id: UUID
    file_name: str
    file_extension: str
    file_bytes: bytes
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
