import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel as PydanticBaseModel, BaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

    def patch_from(self, dao: dict):
        for key, value in dao.items():
            if not hasattr(self, key):
                raise AttributeError(f"Attribute {key} is not exist.")
            self.__setattr__(key, value)
        return self

