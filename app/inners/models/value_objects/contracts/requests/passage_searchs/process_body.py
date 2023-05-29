from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.input_setting_body import InputSettingBody
from app.inners.models.value_objects.contracts.requests.output_setting_body import OutputSettingBody


class ProcessBody(BaseRequest):
    input_setting: InputSettingBody
    output_setting: OutputSettingBody
