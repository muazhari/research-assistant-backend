from __future__ import annotations

from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from app.inners.models.daos.base_dao import BaseDao


class FileDocument(BaseDao, table=True):
    __tablename__ = "file_document"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("document.id"),
            primary_key=True,
        )
    )
    file_name: str
    file_data_hash: str
