from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest

from app.inners.models.value_objects.contracts.requests.managements.accounts.create_body import \
    CreateBody


class CreateOneRequest(BaseRequest):
    body: CreateBody
