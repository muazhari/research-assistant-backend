from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class BaseEmbeddingModelBody(BaseRequest):
    dimension: int
