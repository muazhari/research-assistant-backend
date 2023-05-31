from typing import List

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.basic_settings.dense_retriever_body import DenseRetrieverBody
from app.inners.models.value_objects.contracts.requests.basic_settings.document_setting_body import DocumentSettingBody
from app.inners.models.value_objects.contracts.requests.basic_settings.generator_body import GeneratorBody
from app.inners.models.value_objects.contracts.requests.basic_settings.ranker_body import RankerBody
from app.inners.models.value_objects.contracts.requests.basic_settings.sparse_retriever_body import SparseRetrieverBody


class InputSettingBody(BaseRequest):
    document_setting: DocumentSettingBody
    query: str
    granularity: str
    window_sizes: List[int]
    dense_retriever: DenseRetrieverBody
    sparse_retriever: SparseRetrieverBody
    ranker: RankerBody
