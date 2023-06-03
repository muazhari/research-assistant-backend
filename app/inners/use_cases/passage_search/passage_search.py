import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from haystack import Pipeline
from haystack.document_stores import OpenSearchDocumentStore
from haystack.nodes import BaseRetriever, JoinDocuments, BaseRanker
from haystack.schema import Document as DocumentHaystack

from app.inners.models.entities.document import Document
from app.inners.models.entities.document_type import DocumentType
from app.inners.models.value_objects.contracts.requests.managements.document_types.read_one_by_id_request import \
    ReadOneByIdRequest as DocumentTypeReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.managements.documents.read_one_by_id_request import \
    ReadOneByIdRequest as DocumentReadOneByIdRequest
from app.inners.models.value_objects.contracts.requests.passage_searchs.input_setting_body import InputSettingBody
from app.inners.models.value_objects.contracts.requests.passage_searchs.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.passage_searchs.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.long_form_qas.retrieved_document_response import \
    RetrievedDocumentResponse
from app.inners.models.value_objects.contracts.responses.managements.documents.document_response import DocumentResponse
from app.inners.models.value_objects.contracts.responses.passage_searchs.process_response import ProcessResponse
from app.inners.use_cases.document_conversion.passage_search_document_conversion import PassageSearchDocumentConversion
from app.inners.use_cases.managements.document_management import DocumentManagement
from app.inners.use_cases.managements.document_type_management import DocumentTypeManagement
from app.inners.use_cases.passage_search.ranker_model import RankerModel
from app.inners.use_cases.passage_search.retriever_model import RetrieverModel
from app.inners.use_cases.utilities.document_processor_utility import DocumentProcessorUtility
from app.inners.use_cases.utilities.locker import Locker
from app.outers.settings.datastore_one_setting import DatastoreOneSetting
from app.outers.settings.datastore_two_setting import DatastoreTwoSetting


class PassageSearch:

    def __init__(self):
        self.document_processor_utility = DocumentProcessorUtility()
        self.retriever_model = RetrieverModel()
        self.ranker_model = RankerModel()
        self.datastore_one_setting = DatastoreOneSetting()
        self.datastore_two_setting = DatastoreTwoSetting()
        self.document_management = DocumentManagement()
        self.document_type_management = DocumentTypeManagement()
        self.document_conversion = PassageSearchDocumentConversion()

    async def get_window_sized_documents(self, process_body: ProcessBody) -> List[Document]:
        found_document: Content[Document] = await self.document_management.read_one_by_id(
            request=DocumentReadOneByIdRequest(
                id=process_body.input_setting.document_setting.document_id
            )
        )

        found_document_type: Content[DocumentType] = await self.document_type_management.read_one_by_id(
            request=DocumentTypeReadOneByIdRequest(
                id=found_document.data.document_type_id
            )
        )

        corpus: str = await self.document_conversion.convert_document_to_corpus(
            document_setting_body=process_body.input_setting.document_setting,
            document=found_document.data,
            document_type=found_document_type.data
        )

        window_sized_documents: List[DocumentHaystack] = self.document_processor_utility.process(
            corpus=corpus,
            corpus_source_type=found_document_type.data.name,
            granularity=process_body.input_setting.granularity,
            window_sizes=process_body.input_setting.window_sizes
        )

        os.remove(Path(corpus))

        return window_sized_documents

    def get_document_store_index_hash(self, input_setting: InputSettingBody) -> str:
        hash_source: dict = {
            "document_id": input_setting.document_setting.document_id,
            "granularity": input_setting.granularity,
            "window_sizes": input_setting.window_sizes,
            "embedding_model": input_setting.dense_retriever.embedding_model,
            "similarity_function": input_setting.dense_retriever.similarity_function
        }
        return hashlib.md5(str(hash_source).encode("utf-8")).hexdigest()

    @Locker.wait_lock
    def get_dense_retriever(self, process_body: ProcessBody, documents: List[DocumentHaystack]) -> BaseRetriever:
        document_store_index_hash: str = self.get_document_store_index_hash(
            input_setting=process_body.input_setting
        )

        index: str = f"dense_{document_store_index_hash}"

        document_store: OpenSearchDocumentStore = OpenSearchDocumentStore(
            host=self.datastore_two_setting.DS_2_HOST,
            port=self.datastore_two_setting.DS_2_PORT_1,
            username=self.datastore_two_setting.DS_2_USERNAME,
            password=self.datastore_two_setting.DS_2_PASSWORD,
            index=index,
            embedding_dim=process_body.input_setting.dense_retriever.embedding_model.dimension,
            similarity=process_body.input_setting.dense_retriever.similarity_function,
        )

        retriever: BaseRetriever = self.retriever_model.get_dense_retriever(
            document_store=document_store,
            retriever_body=process_body.input_setting.dense_retriever,
        )

        if process_body.input_setting.dense_retriever.is_update is True:
            document_store.delete_index(index=index)
            document_store.write_documents(documents)
            document_store.update_embeddings(retriever)

        return retriever

    def get_sparse_retriever(self, process_body: ProcessBody, documents: List[Document]) -> BaseRetriever:
        document_store_index_hash: str = self.get_document_store_index_hash(
            input_setting=process_body.input_setting
        )

        document_store: OpenSearchDocumentStore = OpenSearchDocumentStore(
            host=self.datastore_two_setting.DS_2_HOST,
            username=self.datastore_two_setting.DS_2_USERNAME,
            password=self.datastore_two_setting.DS_2_PASSWORD,
            port=self.datastore_two_setting.DS_2_PORT_1,
            index=f"sparse_{document_store_index_hash}",
            similarity=process_body.input_setting.sparse_retriever.similarity_function,
        )
        retriever: BaseRetriever = self.retriever_model.get_sparse_retriever(
            document_store=document_store,
            retriever_body=process_body.input_setting.sparse_retriever,
        )
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

            window_sized_documents: List[DocumentHaystack] = await self.get_window_sized_documents(
                process_body=process_request.body
            )

            pipeline: Pipeline = self.get_pipeline(
                process_body=process_request.body,
                documents=window_sized_documents
            )

            retrieval_result: dict = pipeline.run(
                query=process_request.body.input_setting.query,
                debug=True
            )

            time_finish: datetime = datetime.now()
            time_delta: timedelta = time_finish - time_start

            output_document: DocumentResponse = await self.document_conversion.convert_retrieval_result_to_document(
                process_body=process_request.body,
                retrieval_result=retrieval_result,
                process_duration=time_delta.total_seconds()
            )

            retrieved_documents: List[RetrievedDocumentResponse] = [
                RetrievedDocumentResponse(
                    id=document.id,
                    content=document.content,
                    content_type=document.content_type,
                    meta=document.meta,
                    score=document.score
                )
                for document in
                retrieval_result["_debug"]["Ranker"]["output"]["documents"]
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
