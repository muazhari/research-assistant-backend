from typing import Dict

from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class ReadAllRequest(BaseRequest):
    query_parameter: Dict[str, str]
