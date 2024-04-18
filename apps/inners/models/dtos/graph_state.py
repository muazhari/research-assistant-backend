from typing import TypedDict, List, Union, Optional, Dict
from uuid import UUID

from langchain_community.storage.redis import RedisStore
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from starlette.datastructures import State

from apps.inners.models.dtos.document_category import DocumentCategory
from apps.inners.use_cases.retrievers.hybrid_milvus_retriever import HybridMilvusRetriever
from apps.inners.use_cases.vector_stores.base_milvus_vector_store import BaseMilvusVectorStore


class LlmSettingState(TypedDict):
    model_name: str
    max_token: int
    model: Optional[Union[BaseChatModel]]


class PreprocessorSettingState(TypedDict):
    is_force_refresh_categorized_element: bool
    is_force_refresh_categorized_document: bool
    chunk_size: int
    overlap_size: int
    is_include_table: bool
    is_include_image: bool


class EmbedderSettingState(TypedDict):
    is_force_refresh_embedding: bool
    is_force_refresh_document: bool
    model_name: str
    query_instruction: Optional[str]


class RetrieverSettingState(TypedDict):
    is_force_refresh_relevant_document: bool
    top_k: int
    vector_store: Union[BaseMilvusVectorStore]
    document_store: Union[RedisStore]
    retriever: Union[HybridMilvusRetriever]


class RerankerSettingState(TypedDict):
    is_force_refresh_re_ranked_document: bool
    model_name: str
    top_k: int


class PreparationGraphState(TypedDict):
    state: State
    document_ids: List[UUID]
    llm_setting: LlmSettingState
    preprocessor_setting: PreprocessorSettingState
    categorized_element_hashes: Optional[Dict[UUID, str]]
    categorized_documents: Optional[Dict[UUID, DocumentCategory]]
    categorized_document_hashes: Optional[Dict[UUID, str]]


class PassageSearchGraphState(PreparationGraphState):
    embedder_setting: EmbedderSettingState
    retriever_setting: RetrieverSettingState
    reranker_setting: RerankerSettingState
    question: str
    embedded_document_ids: Optional[List[UUID]]
    relevant_documents: Optional[List[Document]]
    relevant_document_hash: Optional[str]
    re_ranked_documents: Optional[List[Document]]
    re_ranked_document_hash: Optional[str]


class GeneratorSettingState(TypedDict):
    is_force_refresh_generated_answer: bool
    is_force_refresh_generated_question: bool
    is_force_refresh_generated_hallucination_grade: bool
    is_force_refresh_generated_answer_relevancy_grade: bool
    prompt: str


class LongFormQaGraphState(PassageSearchGraphState):
    transform_question_max_retry: int
    generator_setting: GeneratorSettingState
    generated_answer: Optional[str]
    generated_answer_hash: Optional[str]
    generated_question: Optional[str]
    generated_question_hash: Optional[str]
    generated_hallucination_grade: Optional[str]
    generated_hallucination_grade_hash: Optional[str]
    generated_answer_relevancy_grade: Optional[str]
    generated_answer_relevancy_grade_hash: Optional[str]
