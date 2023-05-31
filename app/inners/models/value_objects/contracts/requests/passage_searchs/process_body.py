from uuid import UUID

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.passage_searchs.input_setting_body import InputSettingBody
from app.inners.models.value_objects.contracts.requests.basic_settings.output_setting_body import OutputSettingBody


class ProcessBody(BaseRequest):
    account_id: UUID
    input_setting: InputSettingBody
    output_setting: OutputSettingBody
