from haystack.document_stores import BaseDocumentStore
from haystack.nodes import EmbeddingRetriever, BaseRetriever, DensePassageRetriever, MultihopEmbeddingRetriever, \
    BM25Retriever, TfidfRetriever

from app.inners.models.value_objects.contracts.requests.dense_embedding_model_body import DenseEmbeddingModelBody
from app.inners.models.value_objects.contracts.requests.dense_retriever_body import DenseRetrieverBody
from app.inners.models.value_objects.contracts.requests.multihop_embedding_model_body import MultihopEmbeddingModelBody
from app.inners.models.value_objects.contracts.requests.online_embedding_model_body import OnlineEmbeddingModelBody
from app.inners.models.value_objects.contracts.requests.sparse_retriever_body import SparseRetrieverBody


class RetrieverModel:
    def get_multihop_retriever(self, document_store: BaseDocumentStore,
                               embedding_model_body: MultihopEmbeddingModelBody) -> BaseRetriever:
        retriever: MultihopEmbeddingRetriever = MultihopEmbeddingRetriever(
            document_store=document_store,
            embedding_model=embedding_model_body.model,
            num_iterations=embedding_model_body.num_iterations,
        )
        return retriever

    def get_online_retriever(self, document_store: BaseDocumentStore,
                             embedding_model_body: OnlineEmbeddingModelBody) -> BaseRetriever:
        retriever: EmbeddingRetriever = EmbeddingRetriever(
            document_store=document_store,
            embedding_model=embedding_model_body.model,
            api_key=embedding_model_body.api_key,
        )
        return retriever

    def get_dense_passage_retriever(self, document_store: BaseDocumentStore,
                                    embedding_model_body: DenseEmbeddingModelBody) -> BaseRetriever:
        retriever: DensePassageRetriever = DensePassageRetriever(
            document_store=document_store,
            query_embedding_model=embedding_model_body.query_model,
            passage_embedding_model=embedding_model_body.passage_model,
        )
        return retriever

    def get_bm25_retriever(self, document_store: any) -> BaseRetriever:
        retriever: BM25Retriever = BM25Retriever(
            document_store=document_store
        )
        return retriever

    def get_tfidf_retriever(self, document_store: BaseDocumentStore) -> BaseRetriever:
        retriever: TfidfRetriever = TfidfRetriever(
            document_store=document_store
        )
        return retriever

    def get_dense_retriever(self, document_store: BaseDocumentStore,
                            retriever_body: DenseRetrieverBody) -> BaseRetriever:
        if retriever_body.source_type == "online":
            retriever = self.get_online_retriever(
                document_store=document_store,
                embedding_model_body=retriever_body.embedding_model
            )
        elif retriever_body.source_type == "multihop":
            retriever = self.get_multihop_retriever(
                document_store=document_store,
                embedding_model_body=retriever_body.embedding_model
            )
        elif retriever_body.source_type == "dense_passage":
            retriever = self.get_dense_passage_retriever(
                document_store=document_store,
                embedding_model_body=retriever_body.embedding_model
            )
        else:
            raise ValueError(f"Dense retriever source type {retriever_body.source_type} is not supported.")
        return retriever

    def get_sparse_retriever(self, document_store: BaseDocumentStore,
                             retriever_body: SparseRetrieverBody) -> BaseRetriever:
        if retriever_body.source_type == "tfidf":
            retriever = self.get_tfidf_retriever(
                document_store=document_store,
            )
        elif retriever_body.source_type == "bm25":
            retriever = self.get_bm25_retriever(
                document_store=document_store,
            )
        else:
            raise ValueError(f"Sparse retriever source type {retriever_body.source_type} is not supported.")
        return retriever
