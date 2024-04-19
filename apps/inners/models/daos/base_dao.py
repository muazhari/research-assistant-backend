from sqlmodel import SQLModel

from apps.inners.models.base_model import BaseModelV2


class BaseDao(BaseModelV2, SQLModel):
    pass
