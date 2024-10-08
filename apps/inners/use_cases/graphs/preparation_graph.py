import asyncio
import pickle
from typing import Dict, List, Any, Optional, Coroutine
from uuid import UUID

import litellm
from langchain_community.chat_models import ChatLiteLLM
from langgraph.graph import StateGraph
from starlette.datastructures import State
from unstructured.documents.elements import Element

from apps.inners.exceptions import use_case_exception
from apps.inners.models.daos.document import Document
from apps.inners.models.dtos.constants.document_type_constant import DocumentTypeConstant
from apps.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from apps.inners.models.dtos.contracts.responses.managements.documents.text_document_response import \
    TextDocumentResponse
from apps.inners.models.dtos.contracts.responses.managements.documents.web_document_response import WebDocumentResponse
from apps.inners.models.dtos.document_category import DocumentCategory
from apps.inners.models.dtos.element_category import ElementCategory
from apps.inners.models.dtos.graph_state import PreparationGraphState
from apps.inners.use_cases.document_processor.category_document_processor import CategoryDocumentProcessor
from apps.inners.use_cases.document_processor.partition_document_processor import PartitionDocumentProcessor
from apps.outers.datastores.two_datastore import TwoDatastore
from apps.outers.settings.one_llm_setting import OneLlmSetting
from apps.outers.settings.two_llm_setting import TwoLlmSetting
from tools import cache_tool


class PreparationGraph:
    def __init__(
            self,
            one_llm_setting: OneLlmSetting,
            two_llm_setting: TwoLlmSetting,
            two_datastore: TwoDatastore,
            partition_document_processor: PartitionDocumentProcessor,
            category_document_processor: CategoryDocumentProcessor,
    ):
        self.one_llm_setting = one_llm_setting
        self.two_llm_setting = two_llm_setting
        self.two_datastore = two_datastore
        self.partition_document_processor = partition_document_processor
        self.category_document_processor = category_document_processor
        self.compiled_graph = self.compile()

    def node_get_llm_model(self, input_state: PreparationGraphState) -> PreparationGraphState:
        output_state: PreparationGraphState = input_state

        litellm.anthropic_key = self.one_llm_setting.LLM_ONE_ANTHROPIC_API_KEY_ONE
        litellm.openai_key = self.two_llm_setting.LLM_TWO_OPENAI_API_KEY_ONE
        llm_model: ChatLiteLLM = ChatLiteLLM(
            model=input_state["llm_setting"]["model_name"],
            max_tokens=input_state["llm_setting"]["max_token"],
            streaming=True,
            temperature=0
        )
        output_state["llm_setting"]["model"] = llm_model

        return output_state

    async def node_get_categorized_document_worker(self, input_state: PreparationGraphState,
                                                   document_id: UUID) -> PreparationGraphState:
        output_state: PreparationGraphState = input_state

        categorized_element_hash: str = await self.get_categorized_element_hash(
            state=input_state["state"],
            document_id=document_id,
            file_partition_strategy=input_state["preprocessor_setting"]["file_partition_strategy"]
        )
        categorized_document_hash: str = self.get_categorized_document_hash(
            categorized_element_hash=categorized_element_hash,
            summarization_model_name=input_state["llm_setting"]["model_name"],
            is_include_tables=input_state["preprocessor_setting"]["is_include_table"],
            is_include_images=input_state["preprocessor_setting"]["is_include_image"],
            chunk_size=input_state["preprocessor_setting"]["chunk_size"],
        )

        categorized_element_hashes: Optional[Dict[UUID, str]] = input_state["categorized_element_hashes"]
        if categorized_element_hashes is None:
            output_state["categorized_element_hashes"] = {}
        output_state["categorized_element_hashes"][document_id] = categorized_element_hash
        is_categorized_element_exist: int = await self.two_datastore.async_client.exists(
            categorized_element_hash
        )
        if is_categorized_element_exist == 0:
            is_categorized_element_exist: bool = False
        elif is_categorized_element_exist == 1:
            is_categorized_element_exist: bool = True
        else:
            raise use_case_exception.ExistingCategorizedElementHashInvalid()

        is_force_refresh_categorized_element: bool = input_state["preprocessor_setting"][
            "is_force_refresh_categorized_element"]
        if is_categorized_element_exist is False or is_force_refresh_categorized_element is True:
            elements: List[Element] = await self.partition_document_processor.partition(
                state=input_state["state"],
                document_id=document_id,
                file_partition_strategy=input_state["preprocessor_setting"]["file_partition_strategy"]
            )
            categorized_elements: ElementCategory = await self.category_document_processor.categorize_elements(
                elements=elements
            )
            await self.two_datastore.async_client.set(
                name=categorized_element_hash,
                value=pickle.dumps(categorized_elements)
            )
        else:
            found_categorized_element_bytes: bytes = await self.two_datastore.async_client.get(
                categorized_element_hash
            )
            categorized_elements: ElementCategory = pickle.loads(found_categorized_element_bytes)

        categorized_document_hashes: Optional[Dict[UUID, str]] = input_state["categorized_document_hashes"]
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
                overlap_size=input_state["preprocessor_setting"]["overlap_size"],
                metadata={
                    "document_id": document_id
                }
            )
            await self.two_datastore.async_client.set(
                name=categorized_document_hash,
                value=pickle.dumps(categorized_document)
            )
        else:
            found_categorized_document_bytes: bytes = await self.two_datastore.async_client.get(
                categorized_document_hash
            )
            categorized_document: DocumentCategory = pickle.loads(found_categorized_document_bytes)

        output_state["categorized_documents"][document_id] = categorized_document

        return output_state

    async def node_get_categorized_documents(self, input_state: PreparationGraphState) -> PreparationGraphState:
        output_state: PreparationGraphState = input_state

        document_ids: List[UUID] = input_state["document_ids"]
        output_state["categorized_element_hashes"] = {}
        output_state["categorized_document_hashes"] = {}
        output_state["categorized_documents"] = {}

        future_tasks: List[Coroutine] = []
        for document_id in document_ids:
            future_task = self.node_get_categorized_document_worker(
                input_state=input_state,
                document_id=document_id
            )
            future_tasks.append(future_task)

        for task_result in await asyncio.gather(*future_tasks):
            output_state["categorized_element_hashes"].update(task_result["categorized_element_hashes"])
            output_state["categorized_document_hashes"].update(task_result["categorized_document_hashes"])
            output_state["categorized_documents"].update(task_result["categorized_documents"])

        return output_state

    async def get_categorized_element_hash(
            self,
            state: State,
            document_id: UUID,
            file_partition_strategy: str
    ):
        data: Dict[str, Any] = {
            "document_id": document_id,
        }
        found_document: Document = await self.partition_document_processor.document_management.find_one_by_id_with_authorization(
            state=state,
            id=document_id
        )
        if found_document.document_type_id == DocumentTypeConstant.FILE:
            found_file_document: FileDocumentResponse = await self.partition_document_processor.file_document_management.find_one_by_id_with_authorization(
                state=state,
                id=document_id
            )
            data["document_detail_hash"] = found_file_document.file_data_hash
            data["file_partition_strategy"] = file_partition_strategy
        elif found_document.document_type_id == DocumentTypeConstant.TEXT:
            found_text_document: TextDocumentResponse = await self.partition_document_processor.text_document_management.find_one_by_id_with_authorization(
                state=state,
                id=document_id
            )
            data["document_detail_hash"] = found_text_document.text_content_hash
        elif found_document.document_type_id == DocumentTypeConstant.WEB:
            found_web_document: WebDocumentResponse = await self.partition_document_processor.web_document_management.find_one_by_id_with_authorization(
                state=state,
                id=document_id
            )
            data["document_detail_hash"] = found_web_document.web_url_hash
        else:
            raise use_case_exception.DocumentTypeNotSupported()

        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        hashed_data = f"categorized_element/{hashed_data}"

        return hashed_data

    def get_categorized_document_hash(
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
        hashed_data = f"categorized_document/{hashed_data}"

        return hashed_data

    def compile(self):
        graph: StateGraph = StateGraph(PreparationGraphState)

        graph.add_node(
            node=self.node_get_llm_model.__name__,
            action=self.node_get_llm_model
        )
        graph.add_node(
            node=self.node_get_categorized_documents.__name__,
            action=self.node_get_categorized_documents
        )

        graph.set_entry_point(
            key=self.node_get_llm_model.__name__
        )
        graph.add_edge(
            start_key=self.node_get_llm_model.__name__,
            end_key=self.node_get_categorized_documents.__name__
        )
        graph.set_finish_point(
            key=self.node_get_categorized_documents.__name__
        )

        compiled_graph = graph.compile()

        return compiled_graph
