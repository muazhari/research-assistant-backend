from app.core.model.value_object.search_request import SearchRequest


class SearchFileRequest(SearchRequest):
    file_name: str
    file_extension: str
    file: bytes
