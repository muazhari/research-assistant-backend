from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class PatchOneBody(BaseRequest):
    email: str
    password: str
