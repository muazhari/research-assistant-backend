from uuid import UUID

from app.inners.models.dtos.contracts.responses.base_response import BaseResponse


class TextDocumentResponse(BaseResponse):
    document_id: UUID
    document_type_id: str
    account_id: UUID
    document_name: str
    document_description: str
    text_content: str
    text_content_hash: bytes
