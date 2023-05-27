from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlmodel import Field

from app.inners.models.entities.base_entity import BaseEntity


class Event(BaseEntity, table=True):
    __tablename__ = "event"
    id: UUID = Field(primary_key=True)
    entity_id: UUID
    entity_name: str
    operation: str
    timestamp: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True)))
