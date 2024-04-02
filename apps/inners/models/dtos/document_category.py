from typing import List

from langchain_core.documents import Document

from apps.inners.models.base_model import BaseModelV1


class DocumentCategory(BaseModelV1):
    texts: List[Document]
    tables: List[Document]
    images: List[Document]
    id_key: str
