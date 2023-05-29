from typing import Union

from app.inners.models.value_objects.contracts.requests.base_retriever_body import BaseRetrieverBody
from app.inners.models.value_objects.contracts.requests.dense_embedding_model_body import DenseEmbeddingModelBody
from app.inners.models.value_objects.contracts.requests.multihop_embedding_model_body import MultihopEmbeddingModelBody
from app.inners.models.value_objects.contracts.requests.online_embedding_model_body import OnlineEmbeddingModelBody


class DenseRetrieverBody(BaseRetrieverBody):
    is_update: bool
    source_type: str
    embedding_model: Union[DenseEmbeddingModelBody, MultihopEmbeddingModelBody, OnlineEmbeddingModelBody]
