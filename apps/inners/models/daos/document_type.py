from __future__ import annotations

from sqlmodel import Field

from apps.inners.models.daos.base_dao import BaseDao


class DocumentType(BaseDao, table=True):
    __tablename__ = "document_type"
    id: str = Field(primary_key=True)
    description: str
