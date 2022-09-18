from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.model.entity.base_entity import BaseEntity
from app.core.model.entity.document import Document


class TextDocument(Document):
    text_document_id: Optional[UUID]
    text_content: str
