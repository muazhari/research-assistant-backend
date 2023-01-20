from datetime import timedelta

from app.inner.model.entities.document import Document
from app.outer.interfaces.deliveries.contracts.responses.base_response import BaseResponse


class DocumentTransferDownloadResponse(BaseResponse):
    downloaded_document: Document
    download_duration: timedelta

    class Config:
        json_encoders = {
            timedelta: lambda x: x.total_seconds()
        }
