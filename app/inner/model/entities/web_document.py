from __future__ import annotations

from uuid import UUID

from sqlmodel import Field

from app.inner.model.entities.base_entity import BaseEntity


class WebDocument(BaseEntity, table=True):
    __tablename__ = "web_document"
    id: UUID = Field(primary_key=True)
    document_id: UUID = Field(foreign_key="document.id")
    web_url: str

    def copy(self, *args, sqlmodel=True, **kwargs) -> WebDocument:
        copied_instance = super().copy(*args, **kwargs)
        if sqlmodel:
            copied_instance = WebDocument(**copied_instance.dict())
        return copied_instance
