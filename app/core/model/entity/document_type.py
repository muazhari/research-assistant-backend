from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.model.entity.base_entity import BaseEntity


class DocumentType(BaseEntity):
    id: Optional[UUID]
    name: str
    description: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
