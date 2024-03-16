from __future__ import annotations

from uuid import UUID

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from app.inners.models.daos.base_dao import BaseDao


class Account(BaseDao, table=True):
    __tablename__ = "account"
    id: UUID = Field(sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True))
    email: str
    password: str
