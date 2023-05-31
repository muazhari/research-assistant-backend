from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest


class FileDocumentSettingBody(BaseRequest):
    start_page: int
    end_page: int
