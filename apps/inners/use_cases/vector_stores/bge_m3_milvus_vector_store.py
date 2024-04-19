from typing import Any, Dict, List

from pymilvus import FieldSchema, DataType, CollectionSchema, Hits, AnnSearchRequest, SearchResult, RRFRanker, \
    Collection

from apps.inners.use_cases.embeddings.bge_m3_embedding import BgeM3Embedding
from apps.inners.use_cases.vector_stores.base_milvus_vector_store import BaseMilvusVectorStore


class BgeM3MilvusVectorStore(BaseMilvusVectorStore):

    def __init__(
            self,
            embedding_model: BgeM3Embedding,
            *args: Any,
            sparse_vector_field_name: str = "sparse_vector",
            dense_vector_field_name: str = "dense_vector",
            sparse_vector_index_type: str = "SPARSE_INVERTED_INDEX",
            dense_vector_index_type: str = "GPU_CAGRA",
            **kwargs: Any
    ):
        vector_field_dimensions: Dict[str, Any] = {
            sparse_vector_field_name: embedding_model.dimensions["sparse"],
            dense_vector_field_name: embedding_model.dimensions["dense"]
        }
        kwargs["vector_field_dimensions"] = vector_field_dimensions
        self.embedding_model = embedding_model
        self.sparse_vector_field_name = sparse_vector_field_name
        self.dense_vector_field_name = dense_vector_field_name
        self.sparse_vector_index_type = sparse_vector_index_type
        self.dense_vector_index_type = dense_vector_index_type
        super().__init__(*args, **kwargs)

    def _create_index(self):
        sparse_vector_field_index_params: Dict[str, Any] = self.get_search_params(self.sparse_vector_index_type)
        sparse_vector_field_index_params["index_type"] = self.sparse_vector_index_type
        self.collection.create_index(
            field_name=self.sparse_vector_field_name,
            index_params=sparse_vector_field_index_params
        )
        dense_vector_field_index_params: Dict[str, Any] = self.get_search_params(self.dense_vector_index_type)
        dense_vector_field_index_params["index_type"] = self.dense_vector_index_type
        self.collection.create_index(
            field_name=self.dense_vector_field_name,
            index_params=dense_vector_field_index_params
        )

    def _create_collection(self):
        fields: List[FieldSchema] = [
            FieldSchema(
                name=self.id_field_name,
                dtype=DataType.VARCHAR,
                is_primary=True,
                auto_id=False,
                max_length=65535
            ),
            FieldSchema(
                name=self.sparse_vector_field_name,
                dtype=DataType.SPARSE_FLOAT_VECTOR,
            ),
            FieldSchema(
                name=self.dense_vector_field_name,
                dtype=DataType.FLOAT_VECTOR,
                dim=self.vector_field_dimensions[self.dense_vector_field_name]
            )
        ]

        schema = CollectionSchema(
            fields=fields,
        )

        collection: Collection = Collection(
            name=self.collection_name,
            schema=schema,
            using=self.alias,
            consistency_level=self.consistency_level,
        )
        if self.collection_properties is not None:
            self.collection.set_properties(self.collection_properties)

        return collection

    def embed_texts(
            self,
            texts: List[str],
            ids: List[str],
            batch_size: int = 1000
    ):
        embeddings: Dict[str, Any] = self.embedding_model.encode_documents(texts)

        total_count: int = len(ids)
        for start_index in range(0, total_count, batch_size):
            end_index: int = min(start_index + batch_size, total_count)
            data: List[Any] = [
                ids[start_index:end_index],
                embeddings["sparse"][start_index:end_index],
                embeddings["dense"][start_index:end_index],
            ]
            self.collection.insert(data)

    def search(self, query: str, top_k: int) -> Hits:
        embeddings: Dict[str, Any] = self.embedding_model.encode_queries(texts=[query])

        output_fields = [
            self.id_field_name,
        ]
        search_requests: List[AnnSearchRequest] = [
            AnnSearchRequest(
                data=embeddings["sparse"],
                anns_field=self.sparse_vector_field_name,
                limit=top_k,
                param=self.get_search_params(self.sparse_vector_index_type)
            ),
            AnnSearchRequest(
                data=embeddings["dense"],
                anns_field=self.dense_vector_field_name,
                limit=top_k,
                param=self.get_search_params(self.dense_vector_index_type)
            )
        ]
        search_result: SearchResult = self.collection.hybrid_search(
            reqs=search_requests,
            output_fields=output_fields,
            rerank=RRFRanker(),
            limit=top_k,

        )
        outputs: Hits = search_result[0]

        return outputs
