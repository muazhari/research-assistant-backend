from typing import Union, Optional
from uuid import UUID

from app.inners.models.value_objects.contracts.requests.basic_settings.base_request import BaseRequest
from app.inners.models.value_objects.contracts.requests.basic_settings.file_document_setting_body import \
    FileDocumentSettingBody
from app.inners.models.value_objects.contracts.requests.basic_settings.text_document_setting_body import \
    TextDocumentSettingBody
from app.inners.models.value_objects.contracts.requests.basic_settings.web_document_setting_body import \
    WebDocumentSettingBody


class DocumentSettingBody(BaseRequest):
    document_id: UUID
    detail_setting: Optional[Union[FileDocumentSettingBody, TextDocumentSettingBody, WebDocumentSettingBody]]
    prefix: str
