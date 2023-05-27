from haystack.document_stores import BaseDocumentStore
from haystack.nodes import EmbeddingRetriever, BaseRetriever, DensePassageRetriever, MultihopEmbeddingRetriever, \
    BM25Retriever, TfidfRetriever

from app.inners.models.value_objects.contracts.requests.passage_searchs.process_body import ProcessBody


class RetrieverModel:
    def get_multihop_retriever(self, document_store: BaseDocumentStore,
                               process_body: ProcessBody) -> BaseRetriever:
        retriever: MultihopEmbeddingRetriever = MultihopEmbeddingRetriever(
            document_store=document_store,
            embedding_model=process_body.embedding_model.query_model,
            num_iterations=process_body.num_iterations,
        )
        return retriever

    def get_basic_retriever(self, document_store: BaseDocumentStore,
                            process_body: ProcessBody) -> BaseRetriever:
        retriever: EmbeddingRetriever = EmbeddingRetriever(
            document_store=document_store,
            embedding_model=process_body.embedding_model.query_model,
            api_key=process_body.api_key,
        )
        return retriever

    def get_dense_passage_retriever(self, document_store: BaseDocumentStore,
                                    process_body: ProcessBody) -> BaseRetriever:
        retriever: DensePassageRetriever = DensePassageRetriever(
            document_store=document_store,
            query_embedding_model=process_body.embedding_model.query_model,
            passage_embedding_model=process_body.embedding_model.passage_model,
        )
        return retriever

    def get_bm25_retriever(self, document_store: BaseDocumentStore) -> BaseRetriever:
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
                            process_body: ProcessBody) -> BaseRetriever:
        if process_body.dense_retriever == "basic":
            retriever = self.get_basic_retriever(
                document_store=document_store,
                process_body=process_body
            )
        elif process_body.dense_retriever == "multihop":
            retriever = self.get_multihop_retriever(
                document_store=document_store,
                process_body=process_body
            )
        elif process_body.dense_retriever == "dense_passage":
            retriever = self.get_dense_passage_retriever(
                document_store=document_store,
                process_body=process_body
            )
        else:
            raise ValueError(f"Dense retriever {process_body.dense_retriever} is not supported.")
        return retriever

    def get_sparse_retriever(self, document_store: BaseDocumentStore,
                             process_body: ProcessBody) -> BaseRetriever:
        if process_body.sparse_retriever == "tfidf":
            retriever = self.get_tfidf_retriever(
                document_store=document_store,
            )
        elif process_body.sparse_retriever == "bm25":
            retriever = self.get_bm25_retriever(
                document_store=document_store,
            )
        else:
            raise ValueError(f"Sparse retriever {process_body.sparse_retriever} is not supported.")
        return retriever
