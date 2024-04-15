from uuid import UUID

from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse


class TextDocumentResponse(BaseResponse):
    id: UUID
    document_type_id: str
    account_id: UUID
    name: str
    description: str
    text_content: str
    text_content_hash: str
