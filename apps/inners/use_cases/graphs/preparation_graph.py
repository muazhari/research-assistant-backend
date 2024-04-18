import json
from typing import Dict, List, Any, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from litellm import Router
from unstructured.documents.elements import Element

from apps.inners.exceptions import use_case_exception
from apps.inners.models.dtos.document_category import DocumentCategory
from apps.inners.models.dtos.element_category import ElementCategory
from apps.inners.models.dtos.graph_state import PreparationGraphState
from apps.inners.use_cases.document_processor.category_document_processor import CategoryDocumentProcessor
from apps.inners.use_cases.document_processor.partition_document_processor import PartitionDocumentProcessor
from apps.outers.datastores.two_datastore import TwoDatastore
from apps.outers.settings.one_llm_setting import OneLlmSetting
from tools import cache_tool


class PreparationGraph:
    def __init__(
            self,
            one_llm_setting: OneLlmSetting,
            two_datastore: TwoDatastore,
            partition_document_processor: PartitionDocumentProcessor,
            category_document_processor: CategoryDocumentProcessor,
    ):
        self.one_llm_setting = one_llm_setting
        self.two_datastore = two_datastore
        self.partition_document_processor = partition_document_processor
        self.category_document_processor = category_document_processor
        self.compiled_graph = self._compile_graph()

    def node_get_llm_model(self, input_state: PreparationGraphState) -> PreparationGraphState:
        output_state: PreparationGraphState = input_state

        model_list: List[Dict] = [
            {
                "model_name": "claude-3-haiku-20240307",
                "litellm_params": {
                    "model": "claude-3-haiku-20240307",
                    "api_key": self.one_llm_setting.LLM_ONE_ANTHROPIC_API_KEY_ONE,
                    "provider": "anthropic"
                }
            },
            {
                "model_name": "claude-3-opus-20240229",
                "litellm_params": {
                    "model": "claude-3-opus-20240229",
                    "api_key": self.one_llm_setting.LLM_ONE_ANTHROPIC_API_KEY_ONE,
                    "provider": "anthropic"
                }
            }
        ]
        router: Router = Router(model_list=model_list)
        deployment: Dict[str, Any] = router.get_available_deployment(
            model=input_state["llm_setting"]["model_name"]
        )
        provider: str = deployment["litellm_params"]["provider"]
        if provider == "anthropic":
            llm_model: ChatAnthropic = ChatAnthropic(
                anthropic_api_key=deployment["litellm_params"]["api_key"],
                model=deployment["litellm_params"]["model"],
                max_tokens=input_state["llm_setting"]["max_token"],
                streaming=True,
                temperature=0
            )
        else:
            raise use_case_exception.LlmProviderNotSupported()

        output_state["llm_setting"]["model"] = llm_model

        return output_state

    async def node_get_categorized_documents(self, input_state: PreparationGraphState) -> PreparationGraphState:
        output_state: PreparationGraphState = input_state

        document_id: UUID = input_state["state"].next_document_id

        categorized_element_hash: str = self._get_categorized_element_hash(
            document_id=document_id
        )
        categorized_document_hash: str = self._get_categorized_document_hash(
            categorized_element_hash=categorized_element_hash,
            summarization_model_name=input_state["llm_setting"]["model_name"],
            is_include_tables=input_state["preprocessor_setting"]["is_include_table"],
            is_include_images=input_state["preprocessor_setting"]["is_include_image"],
            chunk_size=input_state["preprocessor_setting"]["chunk_size"],
        )

        categorized_element_hashes: Optional[Dict[UUID, str]] = input_state.get(
            "categorized_element_hashes",
            None
        )
        if categorized_element_hashes is None:
            output_state["categorized_element_hashes"] = {}
        output_state["categorized_element_hashes"][document_id] = categorized_element_hash
        is_categorized_element_exist: bool = cache_tool.is_key_in_cache(
            key=categorized_element_hash
        )
        is_force_refresh_categorized_element: bool = input_state["preprocessor_setting"][
            "is_force_refresh_categorized_element"]
        if is_categorized_element_exist is False or is_force_refresh_categorized_element is True:
            elements: List[Element] = await self.partition_document_processor.partition(
                state=input_state["state"],
                document_id=document_id
            )
            categorized_elements: ElementCategory = await self.category_document_processor.categorize_elements(
                elements=elements
            )
            cache_tool.set_cache(
                key=categorized_element_hash,
                value=categorized_elements,
                timeout=60 * 60 * 24
            )
        else:
            categorized_elements: ElementCategory = cache_tool.get_cache(
                key=categorized_element_hash
            )

        categorized_document_hashes: Optional[Dict[UUID, str]] = input_state.get(
            "categorized_document_hashes",
            None
        )
        if categorized_document_hashes is None:
            output_state["categorized_document_hashes"] = {}
        output_state["categorized_document_hashes"][document_id] = categorized_document_hash
        existing_categorized_document_hash: int = await self.two_datastore.async_client.exists(
            categorized_document_hash
        )
        if existing_categorized_document_hash == 0:
            is_categorized_document_exist: bool = False
        elif existing_categorized_document_hash == 1:
            is_categorized_document_exist: bool = True
        else:
            raise use_case_exception.ExistingCategorizedDocumentHashInvalid()

        is_force_refresh_categorized_document: bool = input_state["preprocessor_setting"][
            "is_force_refresh_categorized_document"]
        if is_categorized_document_exist is False or is_force_refresh_categorized_document is True or is_force_refresh_categorized_element is True:
            categorized_document: DocumentCategory = await self.category_document_processor.get_categorized_documents(
                categorized_elements=categorized_elements,
                summarization_model=input_state["llm_setting"]["model"],
                is_include_table=input_state["preprocessor_setting"]["is_include_table"],
                is_include_image=input_state["preprocessor_setting"]["is_include_image"],
                chunk_size=input_state["preprocessor_setting"]["chunk_size"],
                metadata={
                    "document_id": document_id
                }
            )
            await self.two_datastore.async_client.set(
                name=categorized_document_hash,
                value=json.dumps(categorized_document.dict(), default=jsonable_encoder).encode()
            )
        else:
            found_categorized_document_bytes: bytes = await self.two_datastore.async_client.get(
                categorized_document_hash
            )
            categorized_document: DocumentCategory = DocumentCategory(**json.loads(found_categorized_document_bytes))

        output_state["categorized_documents"][document_id] = categorized_document

        return output_state

    def _get_categorized_element_hash(
            self,
            document_id: UUID,
    ):
        data: Dict[str, Any] = {
            "document_id": document_id,
        }
        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        hashed_data = f"categorized_element-{hashed_data}"

        return hashed_data

    def _get_categorized_document_hash(
            self,
            categorized_element_hash: str,
            summarization_model_name: str,
            is_include_tables: bool,
            is_include_images: bool,
            chunk_size: int,
    ) -> str:
        data: Dict[str, Any] = {
            "categorized_element_hash": categorized_element_hash,
            "summarization_model_name": summarization_model_name,
            "is_include_tables": is_include_tables,
            "is_include_images": is_include_images,
            "chunk_size": chunk_size,
        }
        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        hashed_data = f"categorized_document-{hashed_data}"

        return hashed_data

    async def node_prepare_get_categorized_documents(self, input_state: PreparationGraphState):
        output_state: PreparationGraphState = input_state

        document_ids: List[UUID] = input_state["document_ids"]
        if len(document_ids) == 0:
            raise use_case_exception.DocumentIdsEmpty()

        categorized_documents: Optional[Dict[UUID, DocumentCategory]] = input_state.get(
            "categorized_documents",
            None
        )
        if categorized_documents is None:
            categorized_documents = {}
            output_state["categorized_documents"] = categorized_documents

        next_document_ids: List[UUID] = list(set(document_ids) - set(categorized_documents.keys()))
        next_document_id: UUID = next_document_ids.pop()

        output_state["state"].next_document_id = next_document_id

        return output_state

    async def node_decide_get_categorized_documents_or_embed(self, input_state: PreparationGraphState) -> str:
        output_state: PreparationGraphState = input_state

        document_ids: List[UUID] = input_state["document_ids"]

        categorized_documents: Dict[UUID, DocumentCategory] = input_state["categorized_documents"]

        if set(categorized_documents.keys()) == set(document_ids):
            output_state["state"].next_document_id = None
            return "EMBED"

        return "GET_CATEGORIZED_DOCUMENTS"

    def _compile_graph(self):
        graph: StateGraph = StateGraph(PreparationGraphState)

        graph.add_node(
            key=self.node_get_llm_model.__name__,
            action=self.node_get_llm_model
        )
        graph.add_node(
            key=self.node_prepare_get_categorized_documents.__name__,
            action=self.node_prepare_get_categorized_documents
        )
        graph.add_node(
            key=self.node_get_categorized_documents.__name__,
            action=self.node_get_categorized_documents
        )

        graph.set_entry_point(
            key=self.node_get_llm_model.__name__
        )

        graph.add_edge(
            start_key=self.node_get_llm_model.__name__,
            end_key=self.node_prepare_get_categorized_documents.__name__
        )
        graph.add_edge(
            start_key=self.node_prepare_get_categorized_documents.__name__,
            end_key=self.node_get_categorized_documents.__name__
        )
        graph.add_conditional_edges(
            start_key=self.node_get_categorized_documents.__name__,
            condition=self.node_decide_get_categorized_documents_or_embed,
            conditional_edge_mapping={
                "GET_CATEGORIZED_DOCUMENTS": self.node_prepare_get_categorized_documents.__name__,
                "EMBED": END
            }
        )

        compiled_graph = graph.compile()

        return compiled_graph
