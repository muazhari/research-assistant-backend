from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest

from app.inners.models.value_objects.contracts.requests.managements.text_documents.create_body import \
    CreateBody


class CreateOneRequest(BaseRequest):
    body: CreateBody
