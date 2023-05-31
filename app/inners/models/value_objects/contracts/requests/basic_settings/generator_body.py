from typing import Union

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.basic_settings.online_generator_model_body import \
    OnlineGeneratorModelBody


class GeneratorBody(BaseRequest):
    source_type: str
    generator_model: Union[OnlineGeneratorModelBody]
    prompt: str
    answer_max_length: int
