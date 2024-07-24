from typing import Optional, List, Dict, Any

from FlagEmbedding import FlagLLMReranker, LayerWiseFlagLLMReranker, FlagReranker
from milvus_model.base import RerankResult, BaseRerankFunction

from apps.inners.use_cases.rerankers.base_reranker import BaseReranker


class BgeRerankFunction(BaseRerankFunction):
    def __init__(
            self,
            model_name: str = "BAAI/bge-reranker-v2-m3",
            use_fp16: bool = True,
            batch_size: int = 32,
            normalize: bool = True,
            device: Optional[str] = None,
            cutoff_layers: Optional[List[int]] = None,
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self.normalize = normalize
        self.device = device
        if self.model_name.endswith("m3"):
            self.reranker = FlagReranker(self.model_name, use_fp16=use_fp16, device=self.device)
        elif self.model_name.endswith("gemma"):
            self.reranker = FlagLLMReranker(self.model_name, use_fp16=use_fp16, device=self.device)
        elif self.model_name.endswith("minicpm-layerwise"):
            if cutoff_layers is None:
                self.cutoff_layers = [28]
            self.reranker = LayerWiseFlagLLMReranker(self.model_name, use_fp16=use_fp16, device=self.device)

    def _batchify(self, texts: List[str], batch_size: int) -> List[List[str]]:
        return [texts[i: i + batch_size] for i in range(0, len(texts), batch_size)]

    def __call__(self, query: str, documents: List[str], top_k: int = 5) -> List[RerankResult]:
        batched_texts = self._batchify(documents, self.batch_size)
        scores = []
        for batched_text in batched_texts:
            query_document_pairs = [(query, text) for text in batched_text]
            if type(self.reranker) is LayerWiseFlagLLMReranker:
                batch_score = self.reranker.compute_score(
                    query_document_pairs,
                    normalize=self.normalize,
                    cutoff_layers=self.cutoff_layers
                )
            else:
                batch_score = self.reranker.compute_score(
                    query_document_pairs,
                    normalize=self.normalize
                )
            scores.extend(batch_score)
        ranked_order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        if top_k:
            ranked_order = ranked_order[:top_k]

        results = []
        for index in ranked_order:
            results.append(RerankResult(text=documents[index], score=scores[index], index=index))
        return results


class BgeReranker(BaseReranker):
    """
    For bge-reranker-v2-m3, bge-reranker-v2-gemma, bge-reranker-v2-minicpm-layerwise models only.
    """

    def __init__(
            self,
            model_name: str = "BAAI/bge-reranker-v2-m3",
            use_fp16: bool = True,
            batch_size: int = 32,
            normalize: bool = True,
            cutoff_layers: Optional[List[int]] = None,
            device: Optional[str] = None,
    ):
        self.model_name = model_name
        self.use_fp16 = use_fp16
        self.batch_size = batch_size
        self.normalize = normalize
        self.device = device
        self.model: BgeRerankFunction = BgeRerankFunction(
            model_name=self.model_name,
            use_fp16=self.use_fp16,
            batch_size=self.batch_size,
            normalize=self.normalize,
            cutoff_layers=cutoff_layers,
            device=self.device
        )

    def rerank(self, query: str, texts: List[str], top_k: int) -> List[Dict[str, Any]]:
        results: List[RerankResult] = self.model(
            query=query,
            documents=texts,
            top_k=top_k
        )
        result_dicts: List[Dict[str, Any]] = [result.to_dict() for result in results]

        return result_dicts
