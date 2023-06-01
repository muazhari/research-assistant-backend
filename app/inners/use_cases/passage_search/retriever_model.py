from haystack.document_stores import BaseDocumentStore
from haystack.nodes import EmbeddingRetriever, BaseRetriever, DensePassageRetriever, MultihopEmbeddingRetriever, \
    BM25Retriever, TfidfRetriever

from app.inners.models.value_objects.contracts.requests.basic_settings.dense_retriever_body import DenseRetrieverBody
from app.inners.models.value_objects.contracts.requests.basic_settings.sparse_retriever_body import SparseRetrieverBody


class RetrieverModel:
    def get_multihop_retriever(self, document_store: BaseDocumentStore,
                               retriever_body: DenseRetrieverBody) -> BaseRetriever:
        retriever: MultihopEmbeddingRetriever = MultihopEmbeddingRetriever(
            document_store=document_store,
            embedding_model=retriever_body.embedding_model.model,
            num_iterations=retriever_body.embedding_model.num_iterations,
            top_k=retriever_body.top_k,
        )
        return retriever

    def get_online_retriever(self, document_store: BaseDocumentStore,
                             retriever_body: DenseRetrieverBody) -> BaseRetriever:
        retriever: EmbeddingRetriever = EmbeddingRetriever(
            document_store=document_store,
            embedding_model=retriever_body.embedding_model.model,
            api_key=retriever_body.embedding_model.api_key,
            top_k=retriever_body.top_k,
        )
        return retriever

    def get_dense_passage_retriever(self, document_store: BaseDocumentStore,
                                    retriever_body: DenseRetrieverBody) -> BaseRetriever:
        retriever: DensePassageRetriever = DensePassageRetriever(
            document_store=document_store,
            query_embedding_model=retriever_body.embedding_model.query_model,
            passage_embedding_model=retriever_body.embedding_model.passage_model,
            top_k=retriever_body.top_k,
        )
        return retriever

    def get_bm25_retriever(self, document_store: any, retriever_body: SparseRetrieverBody) -> BaseRetriever:
        retriever: BM25Retriever = BM25Retriever(
            document_store=document_store,
            top_k=retriever_body.top_k
        )
        return retriever

    def get_tfidf_retriever(self, document_store: BaseDocumentStore,
                            retriever_body: SparseRetrieverBody) -> BaseRetriever:
        retriever: TfidfRetriever = TfidfRetriever(
            document_store=document_store,
            top_k=retriever_body.top_k
        )
        return retriever

    def get_dense_retriever(self, document_store: BaseDocumentStore,
                            retriever_body: DenseRetrieverBody) -> BaseRetriever:
        if retriever_body.source_type == "online":
            retriever = self.get_online_retriever(
                document_store=document_store,
                retriever_body=retriever_body
            )
        elif retriever_body.source_type == "multihop":
            retriever = self.get_multihop_retriever(
                document_store=document_store,
                retriever_body=retriever_body
            )
        elif retriever_body.source_type == "dense_passage":
            retriever = self.get_dense_passage_retriever(
                document_store=document_store,
                retriever_body=retriever_body
            )
        else:
            raise NotImplementedError(f"Dense retriever source type {retriever_body.source_type} is not supported.")
        return retriever

    def get_sparse_retriever(self, document_store: BaseDocumentStore,
                             retriever_body: SparseRetrieverBody) -> BaseRetriever:
        if retriever_body.source_type == "local":
            if retriever_body.model == "tfidf":
                retriever = self.get_tfidf_retriever(
                    document_store=document_store,
                    retriever_body=retriever_body
                )
            elif retriever_body.model == "bm25":
                retriever = self.get_bm25_retriever(
                    document_store=document_store,
                    retriever_body=retriever_body
                )
            else:
                raise NotImplementedError(
                    f"Sparse retriever source type {retriever_body.source_type} is not supported.")
        else:
            raise NotImplementedError(f"Sparse retriever source type {retriever_body.source_type} is not supported.")

        return retriever
