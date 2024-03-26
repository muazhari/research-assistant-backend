from uuid import UUID

from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse


class WebDocumentResponse(BaseResponse):
    id: UUID
    document_type_id: str
    document_account_id: UUID
    document_name: str
    document_description: str
    web_url: str
    web_url_hash: str
