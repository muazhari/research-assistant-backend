from uuid import UUID

from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class ReadOneByIdRequest(BaseRequest):
    id: UUID
