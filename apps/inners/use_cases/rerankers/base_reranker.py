from abc import ABC, abstractmethod
from typing import List, Any, Dict


class BaseReranker(ABC):
    @abstractmethod
    def rerank(self, query: str, texts: List[str], top_k: int) -> List[Dict[str, Any]]:
        pass
