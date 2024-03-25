from uuid import UUID

from app.inners.models.dtos.contracts.responses.base_response import BaseResponse


class FileDocumentResponse(BaseResponse):
    id: UUID
    document_type_id: str
    document_account_id: UUID
    document_name: str
    document_description: str
    file_name: str
    file_data_hash: str
    file_meta: dict
