from __future__ import annotations

from uuid import UUID

from sqlmodel import Field

from app.inners.models.entities.base_entity import BaseEntity


class DocumentType(BaseEntity, table=True):
    __tablename__ = "document_type"
    id: UUID = Field(primary_key=True)
    name: str
    description: str
