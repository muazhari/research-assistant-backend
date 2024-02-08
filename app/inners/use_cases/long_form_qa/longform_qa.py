from datetime import datetime, timedelta
from typing import List

from haystack import Pipeline
from haystack.nodes import PromptNode
from haystack.schema import Document as HaystackDocument

from app.inners.models.value_objects.contracts.requests.long_form_qas.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.long_form_qas.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.long_form_qas.process_response import ProcessResponse
from app.inners.models.value_objects.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedDocumentResponse
from app.inners.use_cases.document_conversion.long_form_qa_document_conversion import LongFormQADocumentConversion
from app.inners.use_cases.passage_search.passage_search import PassageSearch


class LongFormQA:
    def __init__(
            self,
            passage_search: PassageSearch,
            long_form_qa_document_conversion: LongFormQADocumentConversion
    ):
        self.passage_search: PassageSearch = passage_search
        self.long_form_qa_document_conversion: LongFormQADocumentConversion = long_form_qa_document_conversion

    def get_pipeline(self, process_body: ProcessBody, documents: List[HaystackDocument]) -> Pipeline:
        generator: PromptNode = self.passage_search.generator_model.get_generator(
            generator_body=process_body.input_setting.generator
        )

        pipeline: Pipeline = self.passage_search.get_pipeline(
            process_body=process_body,
            documents=documents
        )

        pipeline.add_node(
            component=generator,
            name="Generator",
            inputs=["Ranker"]
        )

        return pipeline

    async def qa(self, process_request: ProcessRequest):
        try:
            time_start: datetime = datetime.now()

            processed_query: str = self.passage_search.get_processed_query(
                hyde_setting=process_request.body.input_setting.query_setting.hyde_setting,
                query=process_request.body.input_setting.query,
                prefix=process_request.body.input_setting.query_setting.prefix
            )

            processed_documents: List[HaystackDocument] = await self.passage_search.get_processed_documents(
                document_id=process_request.body.input_setting.document_setting.document_id,
                document_setting_body=process_request.body.input_setting.document_setting,
                granularity=process_request.body.input_setting.granularity,
                window_sizes=process_request.body.input_setting.window_sizes,
                prefix=process_request.body.input_setting.document_setting.prefix
            )

            pipeline: Pipeline = self.get_pipeline(
                process_body=process_request.body,
                documents=processed_documents
            )

            original_query: str = process_request.body.input_setting.query

            generative_result: dict = pipeline.run(
                params={
                    "DenseRetriever": {
                        "query": processed_query,
                    },
                    "SparseRetriever": {
                        "query": processed_query,
                    },
                    "Ranker": {
                        "query": processed_query,
                    },
                    "Generator": {
                        "query": original_query,
                    }
                },
                debug=True
            )

            time_finish: datetime = datetime.now()
            time_delta: timedelta = time_finish - time_start

            deprefixed_documents: List[HaystackDocument] = self.passage_search.document_processor_utility.deprefixer(
                documents=generative_result["_debug"]["Ranker"]["output"]["documents"],
                prefix=process_request.body.input_setting.document_setting.prefix
            )

            retrieved_documents: List[RetrievedDocumentResponse] = [
                RetrievedDocumentResponse(
                    id=document.id,
                    content=document.content,
                    content_type=document.content_type,
                    meta=document.meta,
                    score=document.score
                )
                for document in deprefixed_documents
            ]

            content: Content[ProcessResponse] = Content(
                message="Long form QA succeed.",
                data=ProcessResponse(
                    retrieved_documents=retrieved_documents,
                    generated_answer=generative_result["answers"][0].answer,
                    process_duration=time_delta.total_seconds()
                ),
            )

        except Exception as exception:
            content: Content[ProcessResponse] = Content(
                message=f"Long form QA failed: {exception}",
                data=None,
            )

        return content
