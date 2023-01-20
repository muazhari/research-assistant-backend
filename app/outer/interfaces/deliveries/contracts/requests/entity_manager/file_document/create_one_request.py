from typing import Optional
from uuid import UUID

from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class CreateOneRequest(BaseRequest):
    document_id: Optional[UUID]
    file_name: str
    file_extension: str
    file_bytes: bytes
