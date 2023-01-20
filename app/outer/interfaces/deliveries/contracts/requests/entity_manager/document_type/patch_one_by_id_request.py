from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class PatchOneByIdRequest(BaseRequest):
    name: str
    description: str
