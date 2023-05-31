from uuid import UUID

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.managements.text_documents.patch_body import \
    PatchBody


class PatchOneByIdRequest(BaseRequest):
    id: UUID
    body: PatchBody
