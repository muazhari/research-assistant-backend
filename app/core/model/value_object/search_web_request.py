from app.core.model.value_object.search_request import SearchRequest


class SearchWebRequest(SearchRequest):
    url: str
