from app.inners.models.value_objects.contracts.requests.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.passage_searchs.process_body import ProcessBody


class ProcessRequest(BaseRequest):
    body: ProcessBody
