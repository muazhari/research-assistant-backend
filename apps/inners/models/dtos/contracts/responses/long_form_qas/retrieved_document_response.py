from apps.inners.models.dtos.contracts.responses.base_response import BaseResponse


class RetrievedChunkResponse(BaseResponse):
    text_content: str
    meta: dict
