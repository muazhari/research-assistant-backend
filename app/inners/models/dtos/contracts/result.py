from typing import Generic, TypeVar, Optional

from pydantic.generics import GenericModel

from app.inners.models.dtos.base_dto import BaseDto

T = TypeVar("T")


class Result(BaseDto, GenericModel, Generic[T]):
    status_code: int
    message: str
    data: Optional[T]
