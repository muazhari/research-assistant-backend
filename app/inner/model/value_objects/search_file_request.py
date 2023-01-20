from app.inner.model.value_objects.search_request import SearchRequest


class SearchFileRequest(SearchRequest):
    file_name: str
    file_extension: str
    file: bytes
