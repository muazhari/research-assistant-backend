from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.basic_settings.generator_body import GeneratorBody


class HydeSettingBody(BaseRequest):
    is_use: bool
    generator: GeneratorBody
