from uuid import UUID

from app.inners.models.dtos.contracts.responses.base_response import BaseResponse


class WebDocumentResponse(BaseResponse):
    document_id: UUID
    document_type_id: str
    account_id: UUID
    document_name: str
    document_description: str
    web_url: str
    web_url_hash: bytes
