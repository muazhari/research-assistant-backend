from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.long_form_qas.process_body import ProcessBody


class ProcessRequest(BaseRequest):
    body: ProcessBody
