from datetime import datetime, timedelta
from typing import List

from haystack import Pipeline
from haystack.nodes import PromptNode
from haystack.schema import Document

from app.inners.models.value_objects.contracts.requests.long_form_qas.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.long_form_qas.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.long_form_qas.process_response import ProcessResponse
from app.inners.models.value_objects.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedDocumentResponse
from app.inners.use_cases.document_conversion.long_form_qa_document_conversion import LongFormQADocumentConversion
from app.inners.use_cases.long_form_qa.generator_model import GeneratorModel
from app.inners.use_cases.passage_search.passage_search import PassageSearch


class LongFormQA:
    def __init__(self):
        self.generator_model = GeneratorModel()
        self.passage_search = PassageSearch()
        self.document_conversion = LongFormQADocumentConversion()

    def get_pipeline(self, process_body: ProcessBody, documents: List[Document]) -> Pipeline:
        generator: PromptNode = self.generator_model.get_generator(
            process_body=process_body
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

            window_sized_documents: List[Document] = await self.passage_search.get_window_sized_documents(
                process_body=process_request.body
            )

            pipeline: Pipeline = self.get_pipeline(
                process_body=process_request.body,
                documents=window_sized_documents
            )

            generative_result: dict = pipeline.run(
                query=process_request.body.input_setting.query,
                debug=True
            )

            time_finish: datetime = datetime.now()
            time_delta: timedelta = time_finish - time_start

            retrieved_documents: List[RetrievedDocumentResponse] = [
                RetrievedDocumentResponse(
                    id=document.id,
                    content=document.content,
                    content_type=document.content_type,
                    meta=document.meta,
                    id_hash_keys=document.id_hash_keys,
                    score=document.score
                )
                for document in
                generative_result["_debug"]["Ranker"]["output"]["documents"]
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
