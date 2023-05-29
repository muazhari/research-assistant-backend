from app.inners.models.value_objects.contracts.requests.base_embedding_model_body import BaseEmbeddingModelBody


class MultihopEmbeddingModelBody(BaseEmbeddingModelBody):
    model: str
    num_iterations: int
