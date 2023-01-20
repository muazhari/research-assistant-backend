from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlmodel import Field

from app.inner.model.entities.base_entity import BaseEntity


class Document(BaseEntity, table=True):
    __tablename__ = "document"
    id: UUID = Field(primary_key=True)
    name: str
    description: str
    document_type_id: UUID = Field(foreign_key="document_type.id")
    account_id: UUID = Field(foreign_key="account.id")
    created_at: datetime
    updated_at: datetime

    def copy(self, *args, sqlmodel=True, **kwargs) -> Document:
        copied_instance = super().copy(*args, **kwargs)
        if sqlmodel:
            copied_instance = Document(**copied_instance.dict())
        return copied_instance
