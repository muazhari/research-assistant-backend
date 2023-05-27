from __future__ import annotations

from uuid import UUID

from sqlmodel import Field

from app.inners.models.entities.base_entity import BaseEntity


class Account(BaseEntity, table=True):
    __tablename__ = "account"
    id: UUID = Field(primary_key=True)
    name: str
    password: str
    email: str
