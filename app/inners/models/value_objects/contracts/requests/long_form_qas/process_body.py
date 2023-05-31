from uuid import UUID

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.long_form_qas.input_setting_body import InputSettingBody


class ProcessBody(BaseRequest):
    account_id: UUID
    input_setting: InputSettingBody
