from typing import Union

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.basic_settings.online_ranker_body import OnlineRankerModelBody
from app.inners.models.value_objects.contracts.requests.basic_settings.sentence_transformers_ranker_body import \
    SentenceTransformersRankerModelBody


class RankerBody(BaseRequest):
    source_type: str
    ranker_model: Union[SentenceTransformersRankerModelBody, OnlineRankerModelBody]
    top_k: int
