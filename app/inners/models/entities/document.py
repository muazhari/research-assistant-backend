from __future__ import annotations

from uuid import UUID

from sqlmodel import Field

from app.inners.models.entities.base_entity import BaseEntity


class Document(BaseEntity, table=True):
    __tablename__ = "document"
    id: UUID = Field(primary_key=True)
    name: str
    description: str
    document_type_id: UUID = Field(foreign_key="document_type.id")
    account_id: UUID = Field(foreign_key="account.id")
