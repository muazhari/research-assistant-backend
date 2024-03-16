from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from app.inners.models.daos.base_dao import BaseDao


class Session(BaseDao, table=True):
    __tablename__ = "session"
    id: UUID = Field(sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True))
    account_id: UUID = Field(foreign_key="account.id")
    access_token: str
    refresh_token: str
    access_token_expired_at: datetime
    refresh_token_expired_at: datetime
