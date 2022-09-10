from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.model.entity.base_entity import BaseEntity


class DocumentProcess(BaseEntity):
    id: Optional[UUID]
    from_document_id: UUID
    to_document_id: UUID
    process_duration: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
