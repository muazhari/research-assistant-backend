from typing import Optional, List

from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.embedding_model_body import EmbeddingModelBody


class ProcessBody(BaseRequest):
    corpus_source_type: str
    corpus: str
    query: str
    granularity: str
    window_sizes: List[int]
    retriever_source_type: str
    dense_retriever: str
    sparse_retriever: str
    ranker: str
    embedding_model: EmbeddingModelBody
    embedding_dimension: int
    num_iterations: Optional[int]
    similarity_function: str
    retriever_top_k: float
    ranker_top_k: float
    api_key: Optional[str]
