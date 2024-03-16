from uuid import UUID

from app.inners.models.dtos.contracts.requests.base_request import BaseRequest
from app.inners.models.dtos.contracts.requests.passage_searches.input_setting_body import InputSettingBody
from app.inners.models.dtos.contracts.requests.passage_searches.output_setting_body import OutputSettingBody


class ProcessBody(BaseRequest):
    account_id: UUID
    input_setting: InputSettingBody
    output_setting: OutputSettingBody
