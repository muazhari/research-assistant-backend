from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.model.entity.base_entity import BaseEntity


class Account(BaseEntity):
    id: Optional[UUID]
    name: str
    password: str
    email: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
