from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class BaseRequest(BaseModel):
    class Config:
        json_encoders = {
            UUID: lambda v: str(v)
        }

    def json(self, *args, encoder=jsonable_encoder, **kwargs):
        return super().json(*args, encoder=encoder, **kwargs)
