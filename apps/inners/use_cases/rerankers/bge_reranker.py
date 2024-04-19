from typing import Optional, List, Dict, Any

from milvus_model.base import RerankResult
from milvus_model.reranker import BGERerankFunction

from apps.inners.use_cases.rerankers.base_reranker import BaseReranker


class BgeReranker(BaseReranker):
    """
    For normal reranker only (bge-reranker-base/bge-reranker-large/bge-reranker-v2-m3).
    """

    def __init__(
            self,
            model_name: str = "BAAI/bge-reranker-v2-m3",
            use_fp16: bool = True,
            batch_size: int = 32,
            normalize: bool = True,
            device: Optional[str] = None,
    ):
        self.model_name = model_name
        self.use_fp16 = use_fp16
        self.batch_size = batch_size
        self.normalize = normalize
        self.device = device
        self._reranker_model: BGERerankFunction = BGERerankFunction(
            model_name=self.model_name,
            use_fp16=self.use_fp16,
            batch_size=self.batch_size,
            normalize=self.normalize,
            device=self.device
        )

    def rerank(self, query: str, texts: List[str], top_k: int) -> List[Dict[str, Any]]:
        results: List[RerankResult] = self._reranker_model(
            query=query,
            documents=texts,
            top_k=top_k
        )
        result_dicts: List[Dict[str, Any]] = [result.to_dict() for result in results]

        return result_dicts
