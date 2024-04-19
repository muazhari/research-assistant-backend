from uuid import UUID

from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse


class WebDocumentResponse(BaseResponse):
    id: UUID
    document_type_id: str
    account_id: UUID
    name: str
    description: str
    web_url: str
    web_url_hash: str
