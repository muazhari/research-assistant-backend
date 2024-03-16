from uuid import UUID

from app.inners.models.dtos.contracts.requests.base_request import BaseRequest


class PatchOneBody(BaseRequest):
    name: str
    description: str
    document_type_id: UUID
    account_id: UUID
    file_name: str
    file_extension: str
    file_data: bytes
