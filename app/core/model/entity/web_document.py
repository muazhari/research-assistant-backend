from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.model.entity.base_entity import BaseEntity


class WebDocument(BaseEntity):
    id: Optional[UUID]
    document_id: UUID
    web_url: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
