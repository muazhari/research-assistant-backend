from sqlmodel import SQLModel

from apps.inners.models.base_model import BaseModel


class BaseDao(BaseModel, SQLModel):
    pass
