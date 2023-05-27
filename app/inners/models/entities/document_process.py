from __future__ import annotations

from uuid import UUID

from sqlmodel import Field

from app.inners.models.entities.base_entity import BaseEntity


class DocumentProcess(BaseEntity, table=True):
    __tablename__ = "document_process"
    id: UUID = Field(primary_key=True)
    initial_document_id: UUID = Field(foreign_key="document.id")
    final_document_id: UUID = Field(foreign_key="document.id")
    process_duration: float
