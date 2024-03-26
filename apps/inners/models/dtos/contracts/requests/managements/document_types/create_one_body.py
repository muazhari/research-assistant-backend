from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class CreateOneBody(BaseRequest):
    id: str
    description: str
