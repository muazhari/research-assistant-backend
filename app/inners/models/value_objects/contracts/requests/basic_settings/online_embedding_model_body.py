from app.inners.models.value_objects.contracts.requests.basic_settings.base_embedding_model_body import BaseEmbeddingModelBody


class OnlineEmbeddingModelBody(BaseEmbeddingModelBody):
    model: str
    api_key: str
