from datetime import timedelta

from pydantic import BaseModel

from app.core.model.entity.document import Document


class BaseDocumentSearchResponse(BaseModel):
    processed_document: Document
    process_duration: timedelta

    class Config:
        json_encoders = {
            timedelta: lambda x: x.total_seconds()
        }
