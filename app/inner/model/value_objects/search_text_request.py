from app.inner.model.value_objects.search_request import SearchRequest


class SearchTextRequest(SearchRequest):
    text: str
