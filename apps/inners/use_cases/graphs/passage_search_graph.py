import asyncio
import pickle
from typing import Dict, List, Any, Optional, Tuple
from uuid import UUID

from langchain_community.storage.redis import RedisStore
from langchain_core.documents import Document
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph

from apps.inners.exceptions import use_case_exception
from apps.inners.models.dtos.document_category import DocumentCategory
from apps.inners.models.dtos.graph_state import PassageSearchGraphState
from apps.inners.use_cases.embeddings.bge_m3_embedding import BgeM3Embedding
from apps.inners.use_cases.graphs.preparation_graph import PreparationGraph
from apps.inners.use_cases.rerankers.base_reranker import BaseReranker
from apps.inners.use_cases.rerankers.bge_reranker import BgeReranker
from apps.inners.use_cases.retrievers.hybrid_milvus_retriever import HybridMilvusRetriever
from apps.inners.use_cases.vector_stores.base_milvus_vector_store import BaseMilvusVectorStore
from apps.inners.use_cases.vector_stores.bge_m3_milvus_vector_store import BgeM3MilvusVectorStore
from apps.outers.datastores.four_datastore import FourDatastore
from tools import cache_tool


class PassageSearchGraph(PreparationGraph):
    def __init__(
            self,
            four_datastore: FourDatastore,
            *args: Any,
            **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.four_datastore = four_datastore
        self.compiled_graph: CompiledGraph = self.compile()

    def get_embedding_query(self, embedding_model_name: str, question: str,
                            query_instruction: Optional[str] = None) -> str:
        if embedding_model_name == "BAAI/bge-m3":
            query: str = question
        else:
            raise use_case_exception.EmbeddingModelNameNotSupported()

        return query

    def get_bge_m3_embedding_model(self, model_name: str) -> BgeM3Embedding:
        embedding_model: BgeM3Embedding = BgeM3Embedding(
            model_name=model_name,
            use_fp16=False,
            normalize_embeddings=False,
            return_colbert_vecs=False,
        )

        return embedding_model

    def get_vector_store(self, embedding_model_name: str, collection_name: str, alias: str) -> BaseMilvusVectorStore:
        if embedding_model_name.startswith("BAAI/bge-m3"):
            embedding_model: BgeM3Embedding = cache_tool.get_cache(
                key=f"embedding_model/{embedding_model_name}",
                default_func=lambda: self.get_bge_m3_embedding_model(
                    model_name=embedding_model_name
                )
            )
            vector_store: BgeM3MilvusVectorStore = BgeM3MilvusVectorStore(
                embedding_model=embedding_model,
                alias=alias,
                collection_name=collection_name,
            )
        else:
            raise use_case_exception.EmbeddingModelNameNotSupported()

        return vector_store

    async def node_embed_worker(self, input_state: PassageSearchGraphState,
                                categorized_document: DocumentCategory) -> PassageSearchGraphState:
        output_state: PassageSearchGraphState = input_state

        document_contents: List[str] = []
        document_ids: List[str] = []
        document_key_value_pairs: List[Tuple[Any, Any]] = []
        documents: List[
            Document
        ] = categorized_document.texts + categorized_document.tables + categorized_document.images
        for document in documents:
            document_contents.append(document.page_content)
            document_ids.append(document.metadata[categorized_document.id_key])
            document_key_value_pairs.append(
                (
                    document.metadata[categorized_document.id_key],
                    pickle.dumps(document)
                )
            )

        vector_store: BaseMilvusVectorStore = input_state["retriever_setting"]["vector_store"]
        document_store: RedisStore = input_state["retriever_setting"]["document_store"]

        if len(document_ids) > 0:
            is_collection_exist: bool = vector_store.has_collection()
            is_entity_exist: bool = False
            if is_collection_exist is True:
                existing_entity_ids: List[Dict] = vector_store.collection.query(
                    expr=f"id in {document_ids}"
                )
                if len(existing_entity_ids) == len(document_ids):
                    is_entity_exist: bool = True
            else:
                vector_store.initialize_collection()

            is_force_refresh_embedding: bool = input_state["embedder_setting"]["is_force_refresh_embedding"]
            if is_entity_exist is False or is_force_refresh_embedding is True:
                vector_store.collection.delete(
                    expr=f'id like "%"'
                )
                vector_store.embed_texts(
                    texts=document_contents,
                    ids=document_ids
                )

            existing_document_ids: int = await self.two_datastore.async_client.exists(
                *document_ids
            )
            if existing_document_ids == len(document_ids):
                is_document_exist: bool = True
            else:
                is_document_exist: bool = False

            is_force_refresh_document: bool = input_state["embedder_setting"]["is_force_refresh_document"]
            if is_document_exist is False or is_force_refresh_document is True:
                await document_store.amdelete(keys=document_ids)
                await document_store.amset(key_value_pairs=document_key_value_pairs)

        return output_state

    async def node_embed(self, input_state: PassageSearchGraphState) -> PassageSearchGraphState:
        output_state: PassageSearchGraphState = input_state

        document_store: RedisStore = RedisStore(
            client=self.two_datastore.sync_client
        )
        output_state["retriever_setting"]["document_store"] = document_store
        collection_name: str = self.get_collection_name_hash(
            categorized_document_hashes=input_state["categorized_document_hashes"],
            embedding_model_name=input_state["embedder_setting"]["model_name"]
        )
        vector_store: BaseMilvusVectorStore = self.get_vector_store(
            embedding_model_name=input_state["embedder_setting"]["model_name"],
            collection_name=collection_name,
            alias=self.four_datastore.alias
        )
        output_state["retriever_setting"]["vector_store"] = vector_store

        future_tasks = []
        for categorized_document in input_state["categorized_documents"].values():
            future_task = self.node_embed_worker(
                input_state=input_state,
                categorized_document=categorized_document
            )
            future_tasks.append(future_task)

        await asyncio.gather(*future_tasks)

        return output_state

    def get_collection_name_hash(self, categorized_document_hashes: Dict[UUID, str], embedding_model_name: str) -> str:
        modified_categorized_document_hashes: Dict[str, str] = {}
        for document_id, categorized_document_hash in categorized_document_hashes.items():
            modified_categorized_document_hashes[str(document_id)] = categorized_document_hash
        data: Dict[str, Any] = {
            "categorized_document_hashes": modified_categorized_document_hashes,
            "embedding_model_name": embedding_model_name,
        }
        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        collection_name: str = f"passage_search_{hashed_data}"

        return collection_name

    async def node_get_relevant_documents(self, input_state: PassageSearchGraphState) -> PassageSearchGraphState:
        output_state: PassageSearchGraphState = input_state

        query: str = self.get_embedding_query(
            embedding_model_name=input_state["embedder_setting"]["model_name"],
            query_instruction=input_state["embedder_setting"]["query_instruction"],
            question=input_state["question"]
        )
        vector_store: BaseMilvusVectorStore = input_state["retriever_setting"]["vector_store"]
        document_store: RedisStore = input_state["retriever_setting"]["document_store"]
        retriever: HybridMilvusRetriever = HybridMilvusRetriever(
            vector_store=vector_store,
            document_store=document_store,
            collection_name=vector_store.collection_name,
            search_kwargs={
                "top_k": input_state["retriever_setting"]["top_k"]
            }
        )
        output_state["retriever_setting"]["retriever"] = retriever
        relevant_document_hash: str = self.get_relevant_document_hash(
            top_k=input_state["retriever_setting"]["top_k"],
            collection_name=retriever.vector_store.collection_name,
            query=query,
        )
        existing_relevant_document_hash: int = await self.two_datastore.async_client.exists(relevant_document_hash)
        if existing_relevant_document_hash == 0:
            is_relevant_document_exist: bool = False
        elif existing_relevant_document_hash == 1:
            is_relevant_document_exist: bool = True
        else:
            raise use_case_exception.ExistingRelevantDocumentHashInvalid()

        is_force_refresh_relevant_document: bool = input_state["retriever_setting"][
            "is_force_refresh_relevant_document"]
        is_force_refresh_embedding: bool = input_state["embedder_setting"]["is_force_refresh_embedding"]
        if is_relevant_document_exist is False or is_force_refresh_relevant_document is True or is_force_refresh_embedding is True:
            relevant_documents: List[Document] = await retriever.ainvoke(
                input=query
            )
            await self.two_datastore.async_client.set(
                name=relevant_document_hash,
                value=pickle.dumps(relevant_documents)
            )
        else:
            relevant_document_bytes: bytes = await self.two_datastore.async_client.get(relevant_document_hash)
            relevant_documents: List[Document] = pickle.loads(relevant_document_bytes)

        output_state["relevant_documents"] = relevant_documents
        output_state["relevant_document_hash"] = relevant_document_hash

        return output_state

    def get_relevant_document_hash(self, top_k: int, collection_name: str, query: str) -> str:
        data: Dict[str, Any] = {
            "top_k": top_k,
            "collection_name": collection_name,
            "query": query,
        }
        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        hashed_data = f"relevant_document/{hashed_data}"

        return hashed_data

    def get_reranker_model(self, model_name: str) -> BaseReranker:
        if model_name.startswith("BAAI/bge-reranker"):
            model: BgeReranker = BgeReranker(
                model_name=model_name
            )
        else:
            raise use_case_exception.RerankerModelNameNotSupported()

        return model

    async def node_get_re_ranked_documents(self, input_state: PassageSearchGraphState) -> PassageSearchGraphState:
        output_state: PassageSearchGraphState = input_state

        relevant_document_hash: str = input_state["relevant_document_hash"]
        re_ranked_document_hash: str = self.get_re_ranked_document_hash(
            relevant_document_hash=relevant_document_hash,
            reranker_model_name=input_state["reranker_setting"]["model_name"],
            top_k=input_state["reranker_setting"]["top_k"]
        )
        existing_re_ranked_document_hash: int = await self.two_datastore.async_client.exists(re_ranked_document_hash)
        if existing_re_ranked_document_hash == 0:
            is_re_ranked_document_exist: bool = False
        elif existing_re_ranked_document_hash == 1:
            is_re_ranked_document_exist: bool = True
        else:
            raise use_case_exception.ExistingReRankedDocumentHashInvalid()

        is_force_refresh_re_ranked_document: bool = input_state["reranker_setting"][
            "is_force_refresh_re_ranked_document"]
        if is_re_ranked_document_exist is False or is_force_refresh_re_ranked_document is True:
            relevant_documents: List[Document] = input_state["relevant_documents"]
            reranker_model: BaseReranker = cache_tool.get_cache(
                key=f"reranker_model/{input_state['reranker_setting']['model_name']}",
                default_func=lambda: self.get_reranker_model(
                    model_name=input_state["reranker_setting"]["model_name"]
                )
            )
            texts: List[str] = [document.page_content for document in relevant_documents]
            re_ranked_results: List[Dict[str, Any]] = []
            if len(texts) > 1:
                re_ranked_results += reranker_model.rerank(
                    query=input_state["question"],
                    texts=texts,
                    top_k=input_state["reranker_setting"]["top_k"]
                )
            else:
                re_ranked_results += [
                    {
                        "index": 0,
                        "text": texts[0],
                        "score": 1.0
                    }
                ]
            re_ranked_documents: List[Document] = []
            for re_ranked_result in re_ranked_results:
                relevant_document: Optional[Document] = relevant_documents[re_ranked_result["index"]]
                re_ranked_document: Document = Document(
                    page_content=re_ranked_result["text"],
                    metadata=dict(
                        re_ranked_score=re_ranked_result["score"],
                        **relevant_document.metadata
                    )
                )
                re_ranked_documents.append(re_ranked_document)
            await self.two_datastore.async_client.set(
                name=re_ranked_document_hash,
                value=pickle.dumps(re_ranked_documents)
            )
        else:
            re_ranked_document_bytes: bytes = await self.two_datastore.async_client.get(re_ranked_document_hash)
            re_ranked_documents: List[Document] = pickle.loads(re_ranked_document_bytes)

        output_state["re_ranked_documents"] = re_ranked_documents
        output_state["re_ranked_document_hash"] = re_ranked_document_hash

        return output_state

    def get_re_ranked_document_hash(
            self,
            relevant_document_hash: str,
            reranker_model_name: str,
            top_k: int
    ) -> str:
        data: Dict[str, Any] = {
            "relevant_document_hash": relevant_document_hash,
            "reranker_model_name": reranker_model_name,
            "top_k": top_k
        }
        hashed_data: str = cache_tool.hash_by_dict(
            data=data
        )
        hashed_data = f"re_ranked_document/{hashed_data}"

        return hashed_data

    def compile(self) -> CompiledGraph:
        graph: StateGraph = StateGraph(PassageSearchGraphState)

        graph.add_node(
            node=self.node_get_llm_model.__name__,
            action=self.node_get_llm_model
        )
        graph.add_node(
            node=self.node_get_categorized_documents.__name__,
            action=self.node_get_categorized_documents
        )
        graph.add_node(
            node=self.node_embed.__name__,
            action=self.node_embed
        )
        graph.add_node(
            node=self.node_get_relevant_documents.__name__,
            action=self.node_get_relevant_documents
        )
        graph.add_node(
            node=self.node_get_re_ranked_documents.__name__,
            action=self.node_get_re_ranked_documents
        )

        graph.set_entry_point(
            key=self.node_get_llm_model.__name__
        )
        graph.add_edge(
            start_key=self.node_get_llm_model.__name__,
            end_key=self.node_get_categorized_documents.__name__
        )
        graph.add_edge(
            start_key=self.node_get_categorized_documents.__name__,
            end_key=self.node_embed.__name__,
        )
        graph.add_edge(
            start_key=self.node_embed.__name__,
            end_key=self.node_get_relevant_documents.__name__
        )
        graph.add_edge(
            start_key=self.node_get_relevant_documents.__name__,
            end_key=self.node_get_re_ranked_documents.__name__
        )

        graph.set_finish_point(
            key=self.node_get_re_ranked_documents.__name__
        )

        compiled_graph: CompiledGraph = graph.compile()

        return compiled_graph
