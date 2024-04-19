from typing import Optional
from uuid import UUID

from fastapi import UploadFile

from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest


class PatchOneBody(BaseRequest):
    name: str
    description: str
    account_id: UUID
    file_name: str
    file_data: Optional[UploadFile]
