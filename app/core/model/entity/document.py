from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.model.entity.base_entity import BaseEntity


class Document(BaseEntity):
    id: Optional[UUID]
    name: str
    description: str
    document_type_id: UUID
    account_id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
