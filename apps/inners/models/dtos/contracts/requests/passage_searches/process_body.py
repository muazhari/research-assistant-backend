from apps.inners.models.dtos.contracts.requests.base_request import BaseRequest
from apps.inners.models.dtos.contracts.requests.passage_searches.input_setting_body import InputSettingBody


class ProcessBody(BaseRequest):
    input_setting: InputSettingBody
