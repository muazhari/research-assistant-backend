from __future__ import annotations

from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from app.inners.models.daos.base_dao import BaseDao


class Document(BaseDao, table=True):
    __tablename__ = "document"
    id: UUID = Field(sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True))
    name: str
    description: str
    document_type_id: str = Field(foreign_key="document_type.id")
    account_id: UUID = Field(sa_column=Column(postgresql.UUID(as_uuid=True), ForeignKey("account.id")))
