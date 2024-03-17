from __future__ import annotations

from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from app.inners.models.daos.base_dao import BaseDao


class WebDocument(BaseDao, table=True):
    __tablename__ = "web_document"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("document.id"),
            primary_key=True,
        )
    )
    web_url: str
    web_url_hash: str
