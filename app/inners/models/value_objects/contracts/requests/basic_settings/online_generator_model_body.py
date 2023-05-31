from app.inners.models.value_objects.contracts.requests.basic_settings.base_generator_model_body import \
    BaseGeneratorModelBody


class OnlineGeneratorModelBody(BaseGeneratorModelBody):
    api_key: str
