import hashlib
import os
from datetime import datetime, timedelta
from typing import List

from haystack import Pipeline
from haystack.document_stores import FAISSDocumentStore, InMemoryDocumentStore
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


class PassageSearch:

    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.retriever_model = RetrieverModel()
        self.ranker_model = RankerModel()
        self.datastore_one_setting = DatastoreOneSetting()

    def get_window_sized_documents(self, process_body: ProcessBody) -> List[Document]:
        window_sized_documents: List[Document] = self.document_processor.process(
            corpus=process_body.corpus,
            corpus_source_type=process_body.corpus_source_type,
            granularity=process_body.granularity,
            window_sizes=list(map(int, process_body.window_sizes.split(" ")))
        )

        return window_sized_documents

    def get_document_store_index_hash(self, process_body: ProcessBody) -> str:
        corpus_hash: str = hashlib.md5(process_body.corpus.encode("utf-8")).hexdigest()
        window_sizes_hash: str = hashlib.md5(process_body.window_sizes.encode("utf-8")).hexdigest()
        embedding_model_hash = hashlib.md5(str(process_body.embedding_model).encode("utf-8")).hexdigest()

        document_store_index_hash: str = f"{embedding_model_hash}_{corpus_hash}_{window_sizes_hash}"

        return document_store_index_hash

    @Locker.wait_lock
    def get_dense_retriever(self, process_body: ProcessBody,
                            documents: List[Document]) -> BaseRetriever:
        document_store_index_hash: str = self.get_document_store_index_hash(
            process_body=process_body
        )
        faiss_index_path: str = f"faiss_index_{document_store_index_hash}"
        faiss_config_path: str = f"faiss_config_{document_store_index_hash}"

        if all(map(os.path.exists, [faiss_index_path, faiss_config_path])):
            document_store: FAISSDocumentStore = FAISSDocumentStore.load(
                index_path=faiss_index_path,
                config_path=faiss_config_path,
            )
            retriever: BaseRetriever = self.retriever_model.get_dense_retriever(
                document_store=document_store,
                process_body=process_body,
            )
        else:
            document_store: FAISSDocumentStore = FAISSDocumentStore(
                sql_url=self.datastore_one_setting.URL,
                index=document_store_index_hash,
                embedding_dim=process_body.embedding_dimension,
                return_embedding=True,
                similarity=process_body.similarity_function,
                duplicate_documents="skip",
            )

            retriever: BaseRetriever = self.retriever_model.get_dense_retriever(
                document_store=document_store,
                process_body=process_body,
            )
            document_store.write_documents(documents)
            document_store.update_embeddings(retriever)
            document_store.save(faiss_index_path, faiss_config_path)

        return retriever

    def get_sparse_retriever(self, process_body: ProcessBody,
                             documents: List[Document]) -> BaseRetriever:
        document_store_index_hash: str = self.get_document_store_index_hash(
            process_body=process_body
        )

        document_store: InMemoryDocumentStore = InMemoryDocumentStore(
            index=document_store_index_hash,
            embedding_dim=process_body.embedding_dimension,
            return_embedding=True,
            similarity=process_body.similarity_function,
            duplicate_documents="skip",
            use_bm25=True
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

        pipeline = Pipeline()
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
