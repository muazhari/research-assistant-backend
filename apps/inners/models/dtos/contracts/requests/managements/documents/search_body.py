from typing import Optional

from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class SearchBody(BaseRequest):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    document_type_id: Optional[str]
    account_id: Optional[str]
