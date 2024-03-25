from sqlmodel import SQLModel

from app.inners.models.base_model import BaseModel


class BaseDao(BaseModel, SQLModel):
    pass
