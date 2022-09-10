from datetime import timedelta
from typing import Union

from pydantic import BaseModel

from app.core.model.entity.document import Document
from app.core.model.entity.file_document import FileDocument
from app.core.model.entity.text_document import TextDocument
from app.core.model.entity.web_document import WebDocument


class DocumentSearchResponse(BaseModel):
    processed_document: Document
    process_duration: timedelta

    class Config:
        json_encoders = {
            timedelta: lambda x: x.total_seconds()
        }
