from uuid import UUID

from app.inners.models.dtos.contracts.responses.base_response import BaseResponse


class FileDocumentResponse(BaseResponse):
    document_id: UUID
    document_type_id: str
    account_id: UUID
    document_name: str
    document_description: str
    file_document_id: UUID
    file_name: str
    file_extension: str
    file_content_hash: bytes
    file_meta: dict
