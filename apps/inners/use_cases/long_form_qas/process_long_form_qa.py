from datetime import datetime, timezone
from typing import List

from langchain_core.runnables import RunnableConfig
from starlette.datastructures import State

from apps.inners.models.dtos.contracts.requests.long_form_qas.process_body import ProcessBody
from apps.inners.models.dtos.contracts.responses.long_form_qas.process_response import ProcessResponse
from apps.inners.models.dtos.contracts.responses.passage_searches.process_response import ReRankedDocument
from apps.inners.models.dtos.graph_state import LongFormQaGraphState
from apps.inners.use_cases.graphs.long_form_qa_graph import LongFormQaGraph


class ProcessLongFormQa:
    def __init__(
            self,
            long_form_qa_graph: LongFormQaGraph,
    ):
        self.long_form_qa_graph = long_form_qa_graph

    async def process(self, state: State, body: ProcessBody) -> ProcessResponse:
        started_at: datetime = datetime.now(tz=timezone.utc)
        state.next_document_id = None
        state.next_categorized_document = None
        state.transform_question_current_retry = 0
        input_state: LongFormQaGraphState = {
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
                "overlap_size:": body.input_setting.preprocessor_setting.overlap_size,
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
            "generator_setting": {
                "is_force_refresh_generated_answer": body.input_setting.generator_setting.is_force_refresh_generated_answer,
                "is_force_refresh_generated_question": body.input_setting.generator_setting.is_force_refresh_generated_question,
                "is_force_refresh_generated_hallucination_grade": body.input_setting.generator_setting.is_force_refresh_generated_hallucination_grade,
                "is_force_refresh_generated_answer_relevancy_grade": body.input_setting.generator_setting.is_force_refresh_generated_answer_relevancy_grade,
                "prompt": body.input_setting.generator_setting.prompt,
            },
            "transform_question_max_retry": body.input_setting.transform_question_max_retry,
            "generated_answer": None,
            "generated_answer_hash": None,
            "generated_question": None,
            "generated_question_hash": None,
            "generated_hallucination_grade": None,
            "generated_hallucination_grade_hash": None,
            "generated_answer_relevancy_grade": None,
            "generated_answer_relevancy_grade_hash": None,
        }
        graph_config: RunnableConfig = {
            "recursion_limit": 1000,
        }
        output_state: LongFormQaGraphState = await self.long_form_qa_graph.compiled_graph.ainvoke(
            input=input_state,
            config=graph_config
        )

        re_ranked_document_dicts: List[ReRankedDocument] = [
            ReRankedDocument(**re_ranked_document.dict())
            for re_ranked_document in output_state["re_ranked_documents"]
        ]
        finished_at: datetime = datetime.now(timezone.utc)
        process_response: ProcessResponse = ProcessResponse(
            re_ranked_documents=re_ranked_document_dicts,
            generated_answer=output_state["generated_answer"],
            hallucination_grade=output_state["generated_hallucination_grade"],
            answer_relevancy_grade=output_state["generated_answer_relevancy_grade"],
            started_at=started_at,
            finished_at=finished_at,
        )

        return process_response
