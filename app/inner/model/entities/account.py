from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlmodel import Field

from app.inner.model.entities.base_entity import BaseEntity


class Account(BaseEntity, table=True):
    __tablename__ = "account"
    id: UUID = Field(primary_key=True)
    name: str
    password: str
    email: str
    created_at: datetime
    updated_at: datetime

    def copy(self, *args, sqlmodel=True, **kwargs) -> Account:
        copied_instance = super().copy(*args, **kwargs)
        if sqlmodel:
            copied_instance = Account(**copied_instance.dict())
        return copied_instance
