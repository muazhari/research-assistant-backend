from datetime import timedelta

from pydantic import BaseModel

from app.core.model.entity.document import Document


class DocumentTransferUploadResponse(BaseModel):
    uploaded_document: Document
    upload_duration: timedelta

    class Config:
        json_encoders = {
            timedelta: lambda x: x.total_seconds()
        }
