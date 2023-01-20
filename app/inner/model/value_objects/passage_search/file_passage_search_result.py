from app.outer.interfaces.deliveries.contracts.requests.base_request import BaseRequest


class FilePassageSearchResult(BaseRequest):
    retrieval_result: dict
    file_name: str
    file_extension: str
    file_bytes: bytes
