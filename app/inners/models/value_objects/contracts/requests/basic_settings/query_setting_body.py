from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest


class QuerySettingBody(BaseRequest):
    prefix: str
