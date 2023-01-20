from uuid import UUID

from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class PatchOneByIdRequest(BaseRequest):
    document_id: UUID
    file_name: str
    file_extension: str
    file_bytes: bytes
