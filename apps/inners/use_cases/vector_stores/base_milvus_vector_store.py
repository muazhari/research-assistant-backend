from abc import abstractmethod, ABC
from typing import List, Dict, Any, Optional

from pymilvus import Hits, Collection
from pymilvus.client.types import LoadState
from pymilvus.orm import utility


class BaseMilvusVectorStore(ABC):

    def __init__(
            self,
            collection_name: str,
            vector_field_dimensions: Dict[str, Any],
            alias: str = None,
            consistency_level: str = "Strong",
            collection_properties: Optional[Dict[str, Any]] = None,
            drop_old_collection: bool = False,
            id_field_name: str = "id",
            search_params: Optional[Dict[str, Any]] = None,
    ):
        self.collection_name = collection_name
        self.vector_field_dimensions = vector_field_dimensions
        self.alias = alias
        self.consistency_level = consistency_level
        self.collection_properties = collection_properties
        self.drop_old_collection = drop_old_collection
        self.id_field_name = id_field_name
        self.search_params = search_params
        self._default_search_params = {
            "SPARSE_INVERTED_INDEX": {"metric_type": "IP"},
            "IVF_FLAT": {"metric_type": "IP"},
            "IVF_SQ8": {"metric_type": "IP"},
            "IVF_PQ": {"metric_type": "IP"},
            "HNSW": {"metric_type": "IP"},
            "RHNSW_FLAT": {"metric_type": "IP"},
            "RHNSW_SQ": {"metric_type": "IP"},
            "RHNSW_PQ": {"metric_type": "IP"},
            "IVF_HNSW": {"metric_type": "IP"},
            "ANNOY": {"metric_type": "IP"},
            "SCANN": {"metric_type": "IP"},
            "AUTOINDEX": {"metric_type": "IP"},
            "GPU_CAGRA": {"metric_type": "IP"},
            "GPU_IVF_FLAT": {"metric_type": "IP"},
            "GPU_IVF_PQ": {"metric_type": "IP"},
        }
        self.collection: Optional[Collection] = None
        self.initialize_collection()

    def get_search_params(self, index_type: str) -> Dict[str, Any]:
        if self.search_params is not None:
            return self.search_params
        else:
            return self._default_search_params[index_type]

    def initialize_collection(self):
        if self.has_collection():
            self.collection = Collection(
                self.collection_name,
                using=self.alias,
            )

            if self.collection_properties is not None:
                self.collection.set_properties(self.collection_properties)

            if self.drop_old_collection:
                self.drop_collection()
        else:
            self.collection = None

        if self.collection is None:
            self.collection = self._create_collection()

        self._create_index()

        if utility.load_state(self.collection_name, using=self.alias) == LoadState.NotLoad:
            self.collection.load()

    def drop_collection(self):
        self.collection.drop()
        self.collection = None

    def has_collection(self) -> bool:
        return utility.has_collection(self.collection_name, using=self.alias)

    @abstractmethod
    def _create_index(self):
        pass

    @abstractmethod
    def _create_collection(self):
        pass

    @abstractmethod
    def embed_texts(
            self,
            texts: List[str],
            ids: List[str],
            batch_size: int = 1000
    ):
        pass

    @abstractmethod
    def search(self, query: str, top_k: int) -> Hits:
        pass
