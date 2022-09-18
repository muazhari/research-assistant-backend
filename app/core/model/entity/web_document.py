from typing import Optional
from uuid import UUID

from app.core.model.entity.document import Document


class WebDocument(Document):
    web_document_id: Optional[UUID]
    web_url: str
