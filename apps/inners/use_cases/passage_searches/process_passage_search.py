import io
import uuid
from datetime import datetime, timezone
from typing import List, Tuple, Set, Dict, Any
from uuid import UUID

from fastapi import UploadFile
from langchain_core.runnables import RunnableConfig
from starlette.datastructures import State

from apps.inners.models.daos.document_process import DocumentProcess
from apps.inners.models.dtos.contracts.requests.managements.file_documents.create_one_body import \
    CreateOneBody as FileDocumentCreateOneBody
from apps.inners.models.dtos.contracts.requests.passage_searches.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.managements.documents.file_document_response import \
    FileDocumentResponse
from apps.inners.models.dtos.contracts.responses.passage_searches.process_response import ProcessResponse, \
    ReRankedDocument
from apps.inners.models.dtos.graph_state import PassageSearchGraphState
from apps.inners.use_cases.document_converters.libre_office_document_converter import LibreOfficeDocumentConverter
from apps.inners.use_cases.document_converters.marker_document_converter import MarkerDocumentConverter
from apps.inners.use_cases.graphs.passage_search_graph import PassageSearchGraph
from apps.inners.use_cases.managements.document_process_management import DocumentProcessManagement
from apps.inners.use_cases.managements.file_document_management import FileDocumentManagement


class ProcessPassageSearch:

    def __init__(
            self,
            passage_search_graph: PassageSearchGraph,
            file_document_management: FileDocumentManagement,
            document_process_management: DocumentProcessManagement,
            libre_office_document_converter: LibreOfficeDocumentConverter,
            marker_document_converter: MarkerDocumentConverter,
    ):
        self.passage_search_graph = passage_search_graph
        self.file_document_management = file_document_management
        self.document_process_management = document_process_management
        self.libre_office_document_converter = libre_office_document_converter
        self.marker_document_converter = marker_document_converter

    async def process(self, state: State, body: ProcessBody) -> ProcessResponse:
        started_at: datetime = datetime.now(tz=timezone.utc)
        state.next_document_id = None
        state.current_categorized_document = None
        input_state: PassageSearchGraphState = {
            "state": state,
            "document_ids": body.input_setting.document_ids,
            "llm_setting": {
                "model_name": body.input_setting.llm_setting.model_name,
                "max_token": body.input_setting.llm_setting.max_token,
                "model": None,
            },
            "preprocessor_setting": {
                "is_force_refresh_categorized_element": body.input_setting.preprocessor_setting.is_force_refresh_categorized_element,
                "is_force_refresh_categorized_document": body.input_setting.preprocessor_setting.is_force_refresh_categorized_document,
                "file_partition_strategy": body.input_setting.preprocessor_setting.file_partition_strategy,
                "chunk_size": body.input_setting.preprocessor_setting.chunk_size,
                "overlap_size": body.input_setting.preprocessor_setting.overlap_size,
                "is_include_table": body.input_setting.preprocessor_setting.is_include_table,
                "is_include_image": body.input_setting.preprocessor_setting.is_include_image,
            },
            "categorized_element_hashes": None,
            "categorized_documents": None,
            "categorized_document_hashes": None,
            "embedder_setting": {
                "is_force_refresh_embedding": body.input_setting.embedder_setting.is_force_refresh_embedding,
                "is_force_refresh_document": body.input_setting.embedder_setting.is_force_refresh_document,
                "model_name": body.input_setting.embedder_setting.model_name,
                "query_instruction": body.input_setting.embedder_setting.query_instruction,
            },
            "retriever_setting": {
                "is_force_refresh_relevant_document": body.input_setting.retriever_setting.is_force_refresh_relevant_document,
                "top_k": body.input_setting.retriever_setting.top_k,
            },
            "reranker_setting": {
                "is_force_refresh_re_ranked_document": body.input_setting.reranker_setting.is_force_refresh_re_ranked_document,
                "model_name": body.input_setting.reranker_setting.model_name,
                "top_k": body.input_setting.reranker_setting.top_k,
            },
            "embedded_document_ids": None,
            "relevant_documents": None,
            "relevant_document_hash": None,
            "re_ranked_documents": None,
            "re_ranked_document_hash": None,
            "question": body.input_setting.question,
        }
        graph_config: RunnableConfig = {
            "recursion_limit": 1000,
        }
        output_state: PassageSearchGraphState = await self.passage_search_graph.compiled_graph.ainvoke(
            input=input_state,
            config=graph_config
        )

        finished_at: datetime = datetime.now(timezone.utc)
        document_processes: List[DocumentProcess] = []
        final_document_urls: List[str] = []
        re_ranked_document_ids: Set[UUID] = set([
            re_ranked_document.metadata["document_id"] for re_ranked_document in output_state["re_ranked_documents"]
        ])
        for document_id in re_ranked_document_ids:
            converted_document_data: bytes = await self.libre_office_document_converter.convert_from_document_id(
                state=state,
                document_id=document_id,
                output_format="pdf"
            )
            highlights: List[Tuple[str, str]] = []
            for re_ranked_document in output_state["re_ranked_documents"]:
                score: str = f"{re_ranked_document.metadata['re_ranked_score']:.5f}"
                highlight: Tuple[str, str] = (score, re_ranked_document.page_content)
                highlights.append(highlight)
            marked_document_data: bytes = await self.marker_document_converter.convert_from_data(
                input_file_data=converted_document_data,
                highlights=highlights
            )
            upload_file_data: UploadFile = UploadFile(
                file=io.BytesIO(marked_document_data),
            )
            file_document_creator_body: FileDocumentCreateOneBody = FileDocumentCreateOneBody(
                name=f"Passage Search Marked Document At {started_at}",
                description=f"Origin Document ID: {document_id}",
                account_id=state.authorized_session.account_id,
                file_name=f"{uuid.uuid4()}.pdf",
                file_data=upload_file_data
            )
            file_document_response: FileDocumentResponse = await self.file_document_management.create_one(
                state=state,
                body=file_document_creator_body
            )
            document_process: DocumentProcess = DocumentProcess(
                id=uuid.uuid4(),
                initial_document_id=document_id,
                final_document_id=file_document_response.id,
                started_at=started_at,
                finished_at=finished_at
            )
            document_processes.append(document_process)
            response_headers: Dict[str, Any] = {
                "response-content-type": "application/pdf",
            }
            final_document_url: str = self.file_document_management.file_document_repository.get_object_url(
                object_name=file_document_response.file_name,
                response_headers=response_headers
            )
            final_document_urls.append(final_document_url)

        re_ranked_document_dicts: List[ReRankedDocument] = [
            ReRankedDocument(**re_ranked_document.dict())
            for re_ranked_document in output_state["re_ranked_documents"]
        ]
        process_response: ProcessResponse = ProcessResponse(
            re_ranked_documents=re_ranked_document_dicts,
            document_processes=document_processes,
            final_document_urls=final_document_urls,
            started_at=started_at,
            finished_at=finished_at,
        )

        return process_response
