from typing import Optional
from uuid import UUID

from app.core.model.entity.document import Document


class FileDocument(Document):
    file_document_id: Optional[UUID]
    file_name: str
    file_extension: str
    # base64 encoded bytes
    file_bytes: bytes
