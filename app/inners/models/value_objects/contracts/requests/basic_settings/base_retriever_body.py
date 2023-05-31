from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest


class BaseRetrieverBody(BaseRequest):
    top_k: int
    similarity_function: str
    source_type: str
