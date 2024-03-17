from uuid import UUID

from app.inners.models.dtos.contracts.requests.base_request import BaseRequest


class PatchOneBody(BaseRequest):
    document_name: str
    document_description: str
    document_type_id: str
    document_account_id: UUID
    file_name: str
    file_extension: str
    file_data: bytes
