from typing import Union

from app.inners.models.value_objects.contracts.requests.basic_settings.base_retriever_body import BaseRetrieverBody
from app.inners.models.value_objects.contracts.requests.basic_settings.dense_embedding_model_body import DenseEmbeddingModelBody
from app.inners.models.value_objects.contracts.requests.basic_settings.multihop_embedding_model_body import MultihopEmbeddingModelBody
from app.inners.models.value_objects.contracts.requests.basic_settings.online_embedding_model_body import OnlineEmbeddingModelBody


class DenseRetrieverBody(BaseRetrieverBody):
    is_update: bool
    source_type: str
    embedding_model: Union[DenseEmbeddingModelBody, MultihopEmbeddingModelBody, OnlineEmbeddingModelBody]
