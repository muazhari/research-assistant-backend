import hashlib
from datetime import datetime, timedelta
from typing import List

from haystack import Pipeline
from haystack.document_stores import OpenSearchDocumentStore
from haystack.nodes import BaseRetriever, JoinDocuments, BaseRanker
from haystack.schema import Document

from app.inners.models.value_objects.contracts.requests.passage_searchs.process_body import ProcessBody
from app.inners.models.value_objects.contracts.requests.passage_searchs.process_request import ProcessRequest
from app.inners.models.value_objects.contracts.responses.content import Content
from app.inners.models.value_objects.contracts.responses.passage_search.process_response import ProcessResponse
from app.inners.use_cases.passage_search.ranker_model import RankerModel
from app.inners.use_cases.passage_search.retriever_model import RetrieverModel
from app.inners.use_cases.utilities.document_processor import DocumentProcessor
from app.inners.use_cases.utilities.locker import Locker
from app.outers.settings.datastore_one_setting import DatastoreOneSetting
from app.outers.settings.datastore_two_setting import DatastoreTwoSetting


class PassageSearch:

    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.retriever_model = RetrieverModel()
        self.ranker_model = RankerModel()
        self.datastore_one_setting = DatastoreOneSetting()
        self.datastore_two_setting = DatastoreTwoSetting()

    def get_window_sized_documents(self, process_body: ProcessBody) -> List[Document]:
        window_sized_documents: List[Document] = self.document_processor.process(
            corpus=process_body.corpus,
            corpus_source_type=process_body.corpus_source_type,
            granularity=process_body.granularity,
            window_sizes=process_body.window_sizes
        )

        return window_sized_documents

    def get_document_store_index_hash(self, process_body: ProcessBody) -> str:
        corpus_hash: str = hashlib.md5(process_body.corpus.encode("utf-8")).hexdigest()
        window_sizes_hash: str = hashlib.md5(str(process_body.window_sizes).encode("utf-8")).hexdigest()
        embedding_model_hash = hashlib.md5(str(process_body.embedding_model).encode("utf-8")).hexdigest()

        document_store_index_hash: str = f"{embedding_model_hash}_{corpus_hash}_{window_sizes_hash}"

        return document_store_index_hash

    @Locker.wait_lock
    def get_dense_retriever(self, process_body: ProcessBody,
                            documents: List[Document]) -> BaseRetriever:
        document_store_index_hash: str = self.get_document_store_index_hash(
            process_body=process_body
        )

        document_store: OpenSearchDocumentStore = OpenSearchDocumentStore(
            host=self.datastore_two_setting.DS_2_HOST,
            username=self.datastore_two_setting.DS_2_USERNAME,
            password=self.datastore_two_setting.DS_2_PASSWORD,
            port=self.datastore_two_setting.DS_2_PORT_1,
            index=f"dense_{document_store_index_hash}",
            embedding_dim=process_body.embedding_dimension,
            similarity=process_body.similarity_function,
        )

        retriever: BaseRetriever = self.retriever_model.get_dense_retriever(
            document_store=document_store,
            process_body=process_body,
        )

        return retriever

    def get_sparse_retriever(self, process_body: ProcessBody,
                             documents: List[Document]) -> BaseRetriever:
        document_store_index_hash: str = self.get_document_store_index_hash(
            process_body=process_body
        )

        document_store: OpenSearchDocumentStore = OpenSearchDocumentStore(
            host=self.datastore_two_setting.DS_2_HOST,
            username=self.datastore_two_setting.DS_2_USERNAME,
            password=self.datastore_two_setting.DS_2_PASSWORD,
            port=self.datastore_two_setting.DS_2_PORT_1,
            index=f"sparse_{document_store_index_hash}",
            similarity=process_body.similarity_function,
        )
        retriever: BaseRetriever = self.retriever_model.get_sparse_retriever(
            document_store=document_store,
            process_body=process_body,
        )
        document_store.write_documents(documents)

        return retriever

    def get_ranker(self, process_body: ProcessBody) -> BaseRanker:
        return self.ranker_model.get_ranker(
            process_body=process_body
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
        time_start: datetime = datetime.now()

        window_sized_documents: List[Document] = self.get_window_sized_documents(
            process_body=process_request.body
        )

        pipeline: Pipeline = self.get_pipeline(
            process_body=process_request.body,
            documents=window_sized_documents
        )

        retrieval_result: dict = pipeline.run(
            query=process_request.body.query,
            params={
                "DenseRetriever": {"top_k": process_request.body.retriever_top_k},
                "SparseRetriever": {"top_k": process_request.body.retriever_top_k},
                "Ranker": {"top_k": process_request.body.ranker_top_k}
            },
            debug=True
        )

        time_finish: datetime = datetime.now()
        time_delta: timedelta = time_finish - time_start

        response: ProcessResponse = ProcessResponse(
            retrieval_result=retrieval_result,
            process_duration=time_delta.total_seconds()
        )

        content: Content = Content(
            message="Passage search succeed.",
            data=response,
        )

        return content
