from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class EmbeddingModelBody(BaseRequest):
    query_model: str
    passage_model: str
    ranker_model: str
