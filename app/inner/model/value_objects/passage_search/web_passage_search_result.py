from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class WebPassageSearchResult(BaseRequest):
    retrieval_result: dict
    web_url: str


