from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlmodel import Field

from app.inner.model.entities.base_entity import BaseEntity


class DocumentProcess(BaseEntity, table=True):
    __tablename__ = "document_process"
    id: UUID = Field(primary_key=True)
    initial_document_id: UUID = Field(foreign_key="document.id")
    final_document_id: UUID = Field(foreign_key="document.id")
    process_duration: float
    created_at: datetime
    updated_at: datetime

    def copy(self, *args, sqlmodel=True, **kwargs) -> DocumentProcess:
        copied_instance = super().copy(*args, **kwargs)
        if sqlmodel:
            copied_instance = DocumentProcess(**copied_instance.dict())
        return copied_instance
