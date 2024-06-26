from __future__ import annotations

from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from apps.inners.models.daos.base_dao import BaseDao


class TextDocument(BaseDao, table=True):
    __tablename__ = "text_document"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("document.id"),
            primary_key=True,
        )
    )
    text_content: str
    text_content_hash: str
