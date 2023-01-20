from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlmodel import Field

from app.inner.model.entities.base_entity import BaseEntity


class DocumentType(BaseEntity, table=True):
    __tablename__ = "document_type"
    id: UUID = Field(primary_key=True)
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    def copy(self, *args, sqlmodel=True, **kwargs) -> DocumentType:
        copied_instance = super().copy(*args, **kwargs)
        if sqlmodel:
            copied_instance = DocumentType(**copied_instance.dict())
        return copied_instance
