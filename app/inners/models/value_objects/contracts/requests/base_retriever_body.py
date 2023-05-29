from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class BaseRetrieverBody(BaseRequest):
    similarity_function: str
    source_type: str
    top_k: int
