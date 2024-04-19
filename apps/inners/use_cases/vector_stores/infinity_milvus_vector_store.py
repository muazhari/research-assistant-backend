from typing import Any, Dict, List

from langchain_community.embeddings.infinity import InfinityEmbeddings
from pymilvus import FieldSchema, DataType, CollectionSchema, Hits, SearchResult, Collection

from apps.inners.use_cases.vector_stores.base_milvus_vector_store import BaseMilvusVectorStore


class InfinityMilvusVectorStore(BaseMilvusVectorStore):

    def __init__(
            self,
            embedding_model: InfinityEmbeddings,
            embedding_dimension: int,
            *args: Any,
            dense_vector_field_name: str = "dense_vector",
            dense_vector_index_type: str = "GPU_CAGRA",
            **kwargs: Any
    ):
        vector_field_dimensions: Dict[str, Any] = {
            dense_vector_field_name: embedding_dimension
        }
        kwargs["vector_field_dimensions"] = vector_field_dimensions
        self.embedding_model = embedding_model
        self.dense_vector_field_name = dense_vector_field_name
        self.dense_vector_index_type = dense_vector_index_type
        super().__init__(*args, **kwargs)

    def _create_index(self):
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
        embeddings: List[List[float]] = self.embedding_model.embed_documents(
            texts=texts
        )
        total_count: int = len(ids)
        for start_index in range(0, total_count, batch_size):
            end_index: int = min(start_index + batch_size, total_count)
            data: List[Any] = [
                ids[start_index:end_index],
                embeddings[start_index:end_index],
            ]
            self.collection.insert(data)

    def search(self, query: str, top_k: int) -> Hits:
        embeddings: List[float] = self.embedding_model.embed_query(
            text=query,
        )

        output_fields = [
            self.id_field_name,
        ]
        search_result: SearchResult = self.collection.search(
            data=[embeddings],
            anns_field=self.dense_vector_field_name,
            limit=top_k,
            param=self.get_search_params(self.dense_vector_index_type),
            output_fields=output_fields,
        )
        outputs: Hits = search_result[0]

        return outputs
