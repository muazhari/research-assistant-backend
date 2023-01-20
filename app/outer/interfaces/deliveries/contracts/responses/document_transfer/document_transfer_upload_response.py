from datetime import timedelta

from app.inner.model.entities.document import Document
from app.outer.interfaces.deliveries.contracts.responses.base_response import BaseResponse


class DocumentTransferUploadResponse(BaseResponse):
    uploaded_document: Document
    upload_duration: timedelta

    class Config:
        json_encoders = {
            timedelta: lambda x: x.total_seconds()
        }
