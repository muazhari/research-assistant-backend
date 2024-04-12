from typing import Optional, List, Dict, Any

from milvus_model.hybrid import BGEM3EmbeddingFunction

from apps.inners.use_cases.embeddings.base_embedding import BaseEmbedding


class BgeM3Embedding(BaseEmbedding):

    def __init__(
            self,
            model_name: str = "BAAI/bge-m3",
            batch_size: int = 16,
            device: Optional[str] = None,
            normalize_embeddings: bool = True,
            use_fp16: bool = True,
            return_dense: bool = True,
            return_sparse: bool = True,
            return_colbert_vecs: bool = True,
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self.device = device
        self.normalize_embeddings = normalize_embeddings
        self.use_fp16 = use_fp16
        self.return_dense = return_dense
        self.return_sparse = return_sparse
        self.return_colbert_vecs = return_colbert_vecs
        self._embedding_model: BGEM3EmbeddingFunction = BGEM3EmbeddingFunction(
            model_name=self.model_name,
            batch_size=self.batch_size,
            device=self.device,
            normalize_embeddings=self.normalize_embeddings,
            use_fp16=self.use_fp16,
            return_dense=self.return_dense,
            return_sparse=self.return_sparse,
            return_colbert_vecs=self.return_colbert_vecs,
        )

    def encode_documents(self, texts: List[str]) -> Dict[str, Any]:
        return self._embedding_model.encode_documents(texts)

    def encode_queries(self, texts: List[str]) -> Dict[str, Any]:
        return self._embedding_model.encode_queries(texts)

    @property
    def dimensions(self) -> Dict[str, Any]:
        return self._embedding_model.dim
