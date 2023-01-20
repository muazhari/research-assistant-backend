from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class TextPassageSearchResult(BaseRequest):
    retrieval_result: dict
    text_content: str


