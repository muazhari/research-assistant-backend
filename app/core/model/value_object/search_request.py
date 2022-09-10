from typing import Optional

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    corpus_id: Optional[int]
