from typing import List
from uuid import UUID

from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest


class OutputSettingBody(BaseRequest):
    document_type_id: UUID
