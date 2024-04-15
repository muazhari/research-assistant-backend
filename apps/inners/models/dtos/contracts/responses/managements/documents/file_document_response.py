from uuid import UUID

from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse


class FileDocumentResponse(BaseResponse):
    id: UUID
    document_type_id: str
    account_id: UUID
    name: str
    description: str
    file_name: str
    file_data_hash: str
    file_metadata: dict
