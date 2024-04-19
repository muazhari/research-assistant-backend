import pickle
from typing import Any, Dict, Optional, List

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.stores import BaseStore
from pymilvus import Hits

from apps.inners.exceptions import use_case_exception
from apps.inners.use_cases.vector_stores.base_milvus_vector_store import BaseMilvusVectorStore


class HybridMilvusRetriever(BaseRetriever):
    document_store: BaseStore[str, Document]
    vector_store: BaseMilvusVectorStore
    search_kwargs: Dict[str, Any]
    id_key: Optional[str] = None

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        if self.id_key is None:
            self.id_key = self.vector_store.id_field_name

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        vector_store_retrieved_documents: Hits = self.vector_store.search(
            query=query,
            **self.search_kwargs
        )
        vector_store_retrieved_document_ids: List[str] = [hits.get(self.id_key) for hits in
                                                          vector_store_retrieved_documents]
        document_store_retrieved_documents: List[Optional[bytes]] = self.document_store.mget(
            keys=vector_store_retrieved_document_ids
        )
        decoded_retrieved_documents: List[Document] = []

        for vector_store_retrieved_document, document_store_retrieved_document in zip(
                vector_store_retrieved_documents, document_store_retrieved_documents, strict=True
        ):
            if document_store_retrieved_document is None:
                self.vector_store.collection.delete(
                    expr=f"id in {vector_store_retrieved_document_ids}"
                )
                self.document_store.mdelete(keys=vector_store_retrieved_document_ids)
                raise use_case_exception.DocumentStoreRetrieveError()

            decoded_retrieved_document: Document = pickle.loads(document_store_retrieved_document)
            decoded_retrieved_document.metadata["relevancy_score"] = vector_store_retrieved_document.score
            decoded_retrieved_documents.append(decoded_retrieved_document)

        decoded_retrieved_documents.sort(
            key=lambda x: x.metadata["relevancy_score"],
            reverse=True
        )

        return decoded_retrieved_documents
