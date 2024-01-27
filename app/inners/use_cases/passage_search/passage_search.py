import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List
from uuid import UUID

from haystack import Pipeline
from haystack.document_stores import OpenSearchDocumentStore
from haystack.nodes import BaseRetriever, JoinDocuments, BaseRanker, DenseRetriever, PromptNode
from haystack.schema import Document as HaystackDocument

from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.basic_settings.document_setting_body import DocumentSettingBody
from app.inners.models.value_objects.contracts.requests.managements.document_types.read_one_by_id_request import \
    ReadOneByIdRequest as DocumentTypeReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.read_one_by_id_request import \
    ReadOneByIdRequest as DocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.passage_searches.input_setting_body import InputSettingBody
from app.inners.models.value_objects.contracts.requests.passage_searches.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.passage_searches.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.document_response import DocumentResponse
from app.inners.models.value_objects.contracts.responses.passage_searchs.process_response import ProcessResponse
from app.inners.use_cases.document_conversion.passage_search_document_conversion import PassageSearchDocumentConversion
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.inners.use_cases.passage_search.generator_model import GeneratorModel
from app.inners.use_cases.passage_search.ranker_model import RankerModel
from app.inners.use_cases.passage_search.retriever_model import RetrieverModel
from app.inners.use_cases.utilities.document_processor_utility import DocumentProcessorUtility
from app.inners.use_cases.utilities.query_processor_utility import QueryProcessorUtility
from app.outers.settings.one_datastore_setting import OneDatastoreSetting
from app.outers.settings.two_datastore_setting import TwoDatastoreSetting


class PassageSearch:

    def __init__(
            self,
            document_management: DocumentManagement,
            document_type_management: DocumentTypeManagement,
            retriever_model: RetrieverModel,
            ranker_model: RankerModel,
            generator_model: GeneratorModel,
            passage_search_document_conversion: PassageSearchDocumentConversion,
            query_processor_utility: QueryProcessorUtility,
            document_processor_utility: DocumentProcessorUtility,
            one_datastore_setting: OneDatastoreSetting,
            two_datastore_setting: TwoDatastoreSetting
    ):
        self.document_management: DocumentManagement = document_management
        self.document_type_management: DocumentTypeManagement = document_type_management
        self.retriever_model: RetrieverModel = retriever_model
        self.ranker_model: RankerModel = ranker_model
        self.generator_model: GeneratorModel = generator_model
        self.passage_search_document_conversion: PassageSearchDocumentConversion = passage_search_document_conversion
        self.query_processor_utility: QueryProcessorUtility = query_processor_utility
        self.document_processor_utility: DocumentProcessorUtility = document_processor_utility
        self.one_datastore_setting: OneDatastoreSetting = one_datastore_setting
        self.two_datastore_setting: TwoDatastoreSetting = two_datastore_setting

    def get_processed_query(self, query: str, prefix: str) -> str:
        processed_query: str = self.query_processor_utility.process(
            query=query,
            prefix=prefix
        )

        return processed_query

    async def get_processed_documents(
            self,
            document_id: UUID,
            document_setting_body: DocumentSettingBody,
            granularity: str,
            window_sizes: List[int],
            prefix: str

    ) -> List[Document]:
        found_document: Content[Document] = await self.document_management.read_one_by_id(
            request=DocumentReadOneByIdRequest(
                id=document_id
            )
        )

        found_document_type: Content[DocumentType] = await self.document_type_management.read_one_by_id(
            request=DocumentTypeReadOneByIdRequest(
                id=found_document.data.document_type_id
            )
        )

        corpus: str = await self.passage_search_document_conversion.convert_document_to_corpus(
            document_setting_body=document_setting_body,
            document=found_document.data,
            document_type=found_document_type.data
        )

        processed_documents: List[HaystackDocument] = self.document_processor_utility.process(
            corpus=corpus,
            corpus_source_type=found_document_type.data.name,
            granularity=granularity,
            window_sizes=window_sizes,
            prefix=prefix,
        )

        if found_document_type.data.name == "file":
            os.remove(Path(corpus))

        return processed_documents

    def deprefix_documents(self, documents: List[HaystackDocument], prefix: str) -> List[HaystackDocument]:
        deprefixed_documents: List[HaystackDocument] = []
        for document in documents:
            deprefixed_document: HaystackDocument = HaystackDocument(
                id=document.id,
                content=document.content[len(prefix):],
                content_type=document.content_type,
                meta=document.meta,
                score=document.score
            )
            deprefixed_documents.append(deprefixed_document)

        return deprefixed_documents

    def get_dense_index_hash(self, input_setting: InputSettingBody) -> str:
        hash_source: dict = {
            "document_id": input_setting.document_setting.document_id,
            "granularity": input_setting.granularity,
            "window_sizes": input_setting.window_sizes,
            "prefix": input_setting.document_setting.prefix,
            "embedding_model": input_setting.dense_retriever.embedding_model,
        }
        return hashlib.md5(str(hash_source).encode("utf-8")).hexdigest()

    def get_dense_retriever(self, process_body: ProcessBody, documents: List[HaystackDocument]) -> BaseRetriever:
        index_hash: str = self.get_dense_index_hash(
            input_setting=process_body.input_setting
        )

        index: str = f"dense_{index_hash}"

        document_store: OpenSearchDocumentStore = OpenSearchDocumentStore(
            host=self.two_datastore_setting.DS_2_HOST,
            port=self.two_datastore_setting.DS_2_PORT_1,
            username=self.two_datastore_setting.DS_2_USERNAME,
            password=self.two_datastore_setting.DS_2_PASSWORD,
            index=index,
            embedding_dim=process_body.input_setting.dense_retriever.embedding_model.dimension,
            similarity=process_body.input_setting.dense_retriever.similarity_function,
        )

        retriever: DenseRetriever = self.retriever_model.get_dense_retriever(
            document_store=document_store,
            retriever_body=process_body.input_setting.dense_retriever,
        )

        if process_body.input_setting.dense_retriever.is_refresh is True:
            document_store.delete_index(index=index)
            document_store.write_documents(documents=documents)
            document_store.update_embeddings(retriever=retriever)

        return retriever

    def get_sparse_index_hash(self, input_setting: InputSettingBody) -> str:
        hash_source: dict = {
            "document_id": input_setting.document_setting.document_id,
            "granularity": input_setting.granularity,
            "window_sizes": input_setting.window_sizes,
            "prefix": input_setting.document_setting.prefix,
            "model": input_setting.sparse_retriever.model,
        }
        return hashlib.md5(str(hash_source).encode("utf-8")).hexdigest()

    def get_sparse_retriever(self, process_body: ProcessBody, documents: List[Document]) -> BaseRetriever:
        index_hash: str = self.get_sparse_index_hash(
            input_setting=process_body.input_setting
        )

        index: str = f"sparse_{index_hash}"

        document_store: OpenSearchDocumentStore = OpenSearchDocumentStore(
            host=self.two_datastore_setting.DS_2_HOST,
            username=self.two_datastore_setting.DS_2_USERNAME,
            password=self.two_datastore_setting.DS_2_PASSWORD,
            port=self.two_datastore_setting.DS_2_PORT_1,
            index=index,
            similarity=process_body.input_setting.sparse_retriever.similarity_function,
        )

        retriever: BaseRetriever = self.retriever_model.get_sparse_retriever(
            document_store=document_store,
            retriever_body=process_body.input_setting.sparse_retriever,
        )

        if process_body.input_setting.sparse_retriever.is_refresh is True:
            document_store.delete_index(index=index)
            document_store.write_documents(documents)

        return retriever

    def get_ranker(self, process_body: ProcessBody) -> BaseRanker:
        return self.ranker_model.get_ranker(
            ranker_body=process_body.input_setting.ranker
        )

    def get_pipeline(self, process_body: ProcessBody, documents: List[Document]) -> Pipeline:
        dense_retriever: BaseRetriever = self.get_dense_retriever(
            process_body=process_body,
            documents=documents
        )
        sparse_retriever: BaseRetriever = self.get_sparse_retriever(
            process_body=process_body,
            documents=documents
        )
        document_joiner: JoinDocuments = JoinDocuments(
            join_mode="reciprocal_rank_fusion"
        )
        ranker: BaseRanker = self.get_ranker(
            process_body=process_body
        )

        pipeline: Pipeline = Pipeline()
        pipeline.add_node(
            component=dense_retriever,
            name="DenseRetriever",
            inputs=["Query"]
        )
        pipeline.add_node(
            component=sparse_retriever,
            name="SparseRetriever",
            inputs=["Query"]
        )
        pipeline.add_node(
            component=document_joiner,
            name="DocumentJoiner",
            inputs=["DenseRetriever", "SparseRetriever"]
        )
        pipeline.add_node(
            component=ranker,
            name="Ranker",
            inputs=["DocumentJoiner"]
        )

        return pipeline

    async def search(self, process_request: ProcessRequest) -> Content[ProcessResponse]:
        try:
            time_start: datetime = datetime.now()

            if process_request.body.input_setting.query_setting.hyde_setting.is_use:
                hyde_generator: PromptNode = self.generator_model.get_generator(
                    source_type=process_request.body.input_setting.query_setting.hyde_setting.generator.source_type,
                    generator_body=process_request.body.input_setting.query_setting.hyde_setting.generator
                )
                hyde_query = hyde_generator.run(
                    query=process_request.body.input_setting.query,
                )
                processed_query: str = self.get_processed_query(
                    query=hyde_query[0]["answers"][0].answer,
                    prefix=process_request.body.input_setting.query_setting.prefix
                )
            else:
                processed_query: str = self.get_processed_query(
                    query=process_request.body.input_setting.query,
                    prefix=process_request.body.input_setting.query_setting.prefix
                )

            processed_documents: List[HaystackDocument] = await self.get_processed_documents(
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

            retrieval_result: dict = pipeline.run(
                query=processed_query,
                debug=True
            )

            time_finish: datetime = datetime.now()
            time_delta: timedelta = time_finish - time_start

            output_document: DocumentResponse = await self.passage_search_document_conversion.convert_retrieval_result_to_document(
                process_body=process_request.body,
                retrieval_result=retrieval_result,
                process_duration=time_delta.total_seconds()
            )

            deprefixed_documents: List[HaystackDocument] = self.deprefix_documents(
                documents=retrieval_result["_debug"]["Ranker"]["output"]["documents"],
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
                message="Passage search succeed.",
                data=ProcessResponse(
                    retrieved_documents=retrieved_documents,
                    output_document=output_document,
                    process_duration=time_delta.total_seconds()
                ),
            )
        except Exception as exception:
            content: Content[ProcessResponse] = Content(
                message=f"Passage search failed: {exception}",
                data=None,
            )

        return content
