from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from app.inners.models.daos.base_dao import BaseDao


class DocumentProcess(BaseDao, table=True):
    __tablename__ = "document_process"
    id: UUID = Field(sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True))
    initial_document_id: UUID = Field(sa_column=Column(postgresql.UUID(as_uuid=True), ForeignKey("document.id")))
    final_document_id: UUID = Field(sa_column=Column(postgresql.UUID(as_uuid=True), ForeignKey("document.id")))
    started_at: datetime = Field(sa_column=Column(postgresql.TIMESTAMP(timezone=True)))
    finished_at: datetime = Field(sa_column=Column(postgresql.TIMESTAMP(timezone=True)))
