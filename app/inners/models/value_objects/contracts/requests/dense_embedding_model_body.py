from app.inners.models.value_objects.contracts.requests.base_embedding_model_body import BaseEmbeddingModelBody


class DenseEmbeddingModelBody(BaseEmbeddingModelBody):
    query_model: str
    passage_model: str
