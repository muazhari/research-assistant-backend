from uuid import UUID

from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.managements.accounts.patch_body import \
    PatchBody


class PatchOneByIdRequest(BaseRequest):
    id: UUID
    body: PatchBody
