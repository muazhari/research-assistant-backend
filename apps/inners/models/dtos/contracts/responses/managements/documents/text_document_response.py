from uuid import UUID

from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse


class TextDocumentResponse(BaseResponse):
    id: UUID
    document_type_id: str
    document_account_id: UUID
    document_name: str
    document_description: str
    text_content: str
    text_content_hash: str
