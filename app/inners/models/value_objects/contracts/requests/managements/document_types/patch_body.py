from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class PatchBody(BaseRequest):
    name: str
    description: str
