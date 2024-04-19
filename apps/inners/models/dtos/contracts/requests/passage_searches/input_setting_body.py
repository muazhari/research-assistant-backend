from typing import List, Optional
from uuid import UUID

from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class LlmSetting(BaseRequest):
    model_name: str
    max_token: int


class PreprocessorSetting(BaseRequest):
    is_force_refresh_categorized_element: bool
    is_force_refresh_categorized_document: bool
    file_partition_strategy: str
    chunk_size: int
    overlap_size: int
    is_include_table: bool
    is_include_image: bool


class EmbedderSetting(BaseRequest):
    is_force_refresh_embedding: bool
    is_force_refresh_document: bool
    model_name: str
    query_instruction: Optional[str]


class RetrieverSetting(BaseRequest):
    is_force_refresh_relevant_document: bool
    top_k: int


class RerankerSetting(BaseRequest):
    is_force_refresh_re_ranked_document: bool
    model_name: str
    top_k: int


class InputSettingBody(BaseRequest):
    document_ids: List[UUID]
    llm_setting: LlmSetting
    preprocessor_setting: PreprocessorSetting
    embedder_setting: EmbedderSetting
    retriever_setting: RetrieverSetting
    reranker_setting: RerankerSetting
    question: str
