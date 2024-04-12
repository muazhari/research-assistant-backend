from abc import abstractmethod, ABC
from typing import List, Union, Any, Dict


class BaseEmbedding(ABC):
    @abstractmethod
    def encode_documents(self, texts: List[str]) -> Union[List[Any], Dict[str, Any]]:
        pass

    @abstractmethod
    def encode_queries(self, texts: List[str]) -> Union[List[Any], Dict[str, Any]]:
        pass