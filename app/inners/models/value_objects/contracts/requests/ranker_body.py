from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class RankerBody(BaseRequest):
    source_type: str
    model: str
    top_k: int
