from typing import List
from uuid import UUID

from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.dense_retriever_body import DenseRetrieverBody
from app.inners.models.value_objects.contracts.requests.ranker_body import RankerBody
from app.inners.models.value_objects.contracts.requests.sparse_retriever_body import SparseRetrieverBody


class InputSettingBody(BaseRequest):
    document_id: UUID
    query: str
    granularity: str
    window_sizes: List[int]
    dense_retriever: DenseRetrieverBody
    sparse_retriever: SparseRetrieverBody
    ranker: RankerBody
