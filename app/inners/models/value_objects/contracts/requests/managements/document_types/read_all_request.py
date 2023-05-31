from typing import Dict

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest


class ReadAllRequest(BaseRequest):
    query_parameter: Dict[str, str]
