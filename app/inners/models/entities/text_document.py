from __future__ import annotations

from uuid import UUID

from sqlmodel import Field

from app.inners.models.entities.base_entity import BaseEntity


class TextDocument(BaseEntity, table=True):
    __tablename__ = "text_document"
    id: UUID = Field(primary_key=True)
    document_id: UUID = Field(foreign_key="document.id")
    text_content: str
