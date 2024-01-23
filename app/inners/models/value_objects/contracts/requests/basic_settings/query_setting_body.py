from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.basic_settings.hyde_setting_body import HydeSettingBody


class QuerySettingBody(BaseRequest):
    prefix: str
    hyde_setting: HydeSettingBody
