from app.inners.models.value_objects.contracts.requests.basic_settings.base_ranker_model_body import BaseRankerModelBody


class OnlineRankerModelBody(BaseRankerModelBody):
    api_key: str
